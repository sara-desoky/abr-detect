from __future__ import annotations

import os
import random
import re
import threading
import time
from typing import Optional

import serial

from nanovna_backend import resonance_from_scan


class HeaterExperimentController:
    """
    Coordinates Arduino heater control and VNA stability streaming.

    Protocol sent to Arduino:
    - "START\\n" to start heater/fan PI loop.
    - "STOP\\n" to stop heater/fan.
    - "VNA:<freq_mhz>\\n" for each resonance reading in MHz.
    """

    def __init__(
        self,
        sim_mode: bool,
        arduino_port: str | None = None,
        arduino_baud: int = 115200,
        nanovna_port: str | None = None,
        sample_interval_s: float = 20.0,
    ):
        self.sim_mode = sim_mode
        self.arduino_port = arduino_port or os.getenv("ARDUINO_PORT", "/dev/ttyUSB0")
        self.arduino_baud = arduino_baud
        self.nanovna_port = nanovna_port or os.getenv("NANOVNA_PORT", "/dev/ttyACM0")
        self.sample_interval_s = sample_interval_s

        self._arduino: Optional[serial.Serial] = None
        self._arduino_lock = threading.Lock()

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_evt = threading.Event()

        self._sim_mhz = 725.99
        self._sim_collection_idx = 0

        self._esbl_threshold_hz = -30_000.0
        if self.sim_mode:
            self.sample_interval_s = 5.0
            self._collection_duration_s = 10.0
        else:
            self._collection_duration_s = 12.0 * 60.0
        self._baseline_required_points = 3
        # Sim mode keeps short timing, but should use real NanoVNA by default.
        # Set ABR_SIM_FAKE_VNA=1 to force synthetic readings.
        self._sim_fake_vna = os.getenv("ABR_SIM_FAKE_VNA", "0") in {"1", "true", "True"}

        self._baseline_active = False
        self._baseline_done = False
        self._baseline_readings: list[tuple[float, float]] = []
        self._baseline_hz: Optional[float] = None

        self._collection_active = False
        self._collection_done = False
        self._collection_started_at: Optional[float] = None
        self._collection_readings: list[tuple[float, float]] = []
        self._result: Optional[dict] = None
        self._result_lock = threading.Lock()

        self._target_temp_c = 25.0
        self._temp_ready_deadband_c = 0.2
        self._stable_required = 10
        self._stable_thresh_mhz = 0.03
        self._current_temp_c: Optional[float] = None
        self._vna_stable_count = 0
        self._last_vna_mhz: Optional[float] = None
        self._state_lock = threading.Lock()

    @property
    def running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            return

        if self.sim_mode:
            # In simulation mode, still try to drive the real heater for demos.
            # If Arduino is unavailable, continue with simulated flow.
            try:
                self._open_arduino()
                self._send_line("START")
            except Exception:
                pass
        else:
            self._open_arduino()
            self._send_line("START")

        self._stop_evt.clear()
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self._running and self._arduino is None:
            return

        self._stop_evt.set()
        self._running = False

        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

        try:
            self._send_line("STOP")
        finally:
            self._close_arduino()

    def begin_collection_window(self) -> None:
        with self._result_lock:
            self._collection_active = True
            self._collection_done = False
            self._collection_started_at = time.time()
            self._collection_readings = []
            self._result = None
            self._sim_collection_idx = 0

    def begin_baseline_window(self) -> None:
        with self._result_lock:
            self._baseline_active = True
            self._baseline_done = False
            self._baseline_readings = []
            self._baseline_hz = None

    def baseline_progress(self) -> dict:
        with self._result_lock:
            got = len(self._baseline_readings)
            need = self._baseline_required_points
            pct = min(100.0, (float(got) / float(need)) * 100.0) if need > 0 else 100.0
            return {
                "active": self._baseline_active,
                "done": self._baseline_done,
                "points": got,
                "required_points": need,
                "pct": pct,
                "baseline_hz": self._baseline_hz,
            }

    def collection_progress(self) -> dict:
        with self._result_lock:
            if self._collection_started_at is None:
                return {
                    "started": False,
                    "done": False,
                    "elapsed_s": 0.0,
                    "duration_s": self._collection_duration_s,
                    "pct": 0.0,
                    "points": 0,
                }

            elapsed = max(0.0, time.time() - self._collection_started_at)
            if self._collection_active and elapsed >= self._collection_duration_s:
                self._collection_active = False
                self._collection_done = True
            pct = min(100.0, (elapsed / self._collection_duration_s) * 100.0)
            return {
                "started": True,
                "done": self._collection_done,
                "elapsed_s": elapsed,
                "duration_s": self._collection_duration_s,
                "pct": pct,
                "points": len(self._collection_readings),
            }

    def finalize_collection_result(self) -> dict:
        with self._result_lock:
            if self._result is not None:
                return dict(self._result)

        result = self._compute_esbl_result()
        with self._result_lock:
            self._result = dict(result)
            return dict(self._result)

    def latest_result(self) -> Optional[dict]:
        with self._result_lock:
            if self._result is None:
                return None
            return dict(self._result)

    def preheat_progress(self) -> dict:
        with self._state_lock:
            current = self._current_temp_c
            stable_got = self._vna_stable_count
            stable_need = self._stable_required

        temp_ready = (
            current is not None
            and abs(current - self._target_temp_c) <= self._temp_ready_deadband_c
        )
        stable_ready = stable_got >= stable_need
        return {
            "current_c": current,
            "target_c": self._target_temp_c,
            "stable_got": min(stable_got, stable_need),
            "stable_need": stable_need,
            "temp_ready": temp_ready,
            "stable_ready": stable_ready,
        }

    def _open_arduino(self) -> None:
        if self._arduino is not None and self._arduino.is_open:
            return

        self._arduino = serial.Serial(self.arduino_port, self.arduino_baud, timeout=0.5)
        # CH340/ATmega boards can reset on open.
        time.sleep(2.0)
        self._arduino.reset_input_buffer()
        self._arduino.reset_output_buffer()

    def _close_arduino(self) -> None:
        with self._arduino_lock:
            if self._arduino is not None:
                try:
                    self._arduino.close()
                except Exception:
                    pass
            self._arduino = None

    def _send_line(self, text: str) -> None:
        with self._arduino_lock:
            if self._arduino is None or not self._arduino.is_open:
                return
            self._arduino.write((text + "\n").encode("utf-8"))

    def _poll_arduino_status(self) -> None:
        with self._arduino_lock:
            if self._arduino is None or not self._arduino.is_open:
                return
            s = self._arduino
            try:
                while s.in_waiting > 0:
                    line = s.readline().decode("utf-8", errors="ignore").strip()
                    if not line:
                        continue
                    m = re.search(r"T2:\s*([-+]?\d+(?:\.\d+)?)", line)
                    if m:
                        try:
                            t2 = float(m.group(1))
                            with self._state_lock:
                                self._current_temp_c = t2
                        except Exception:
                            pass
            except Exception:
                pass

    def _update_vna_stability(self, freq_mhz: float) -> None:
        with self._state_lock:
            if self._last_vna_mhz is None:
                self._vna_stable_count = 1
            else:
                if abs(freq_mhz - self._last_vna_mhz) <= self._stable_thresh_mhz:
                    self._vna_stable_count += 1
                else:
                    self._vna_stable_count = 1
            self._last_vna_mhz = freq_mhz

    def _read_resonance_mhz(self) -> Optional[float]:
        if self.sim_mode and self._sim_fake_vna:
            if self._collection_active:
                # Sim-mode profile: stable region before PenG effect, then a drop.
                if self._sim_collection_idx < 2:
                    self._sim_mhz = 725.99 + random.uniform(-0.01, 0.01)
                else:
                    self._sim_mhz = 725.72 + random.uniform(-0.02, 0.02)
                self._sim_collection_idx += 1
            else:
                self._sim_mhz = 725.99 + random.uniform(-0.006, 0.006)
            return self._sim_mhz

        try:
            result = resonance_from_scan(
                port=self.nanovna_port,
                start_hz=650_000_000,
                stop_hz=820_000_000,
                points=401,
                trace=1,
            )
            return result.f_res_hz / 1_000_000.0
        except Exception:
            if self.sim_mode:
                # If real NanoVNA is unavailable during sim demos, fall back to synthetic.
                if self._collection_active:
                    if self._sim_collection_idx < 2:
                        self._sim_mhz = 725.99 + random.uniform(-0.01, 0.01)
                    else:
                        self._sim_mhz = 725.72 + random.uniform(-0.02, 0.02)
                    self._sim_collection_idx += 1
                else:
                    self._sim_mhz = 725.99 + random.uniform(-0.006, 0.006)
                return self._sim_mhz
            return None

    def _monitor_loop(self) -> None:
        while not self._stop_evt.is_set():
            self._poll_arduino_status()
            freq_mhz = self._read_resonance_mhz()
            if freq_mhz is not None:
                self._send_line(f"VNA:{freq_mhz:.6f}")
                self._update_vna_stability(freq_mhz)
                self._maybe_record_baseline_point(freq_mhz)
                self._maybe_record_collection_point(freq_mhz)

            time.sleep(self.sample_interval_s)

    def _maybe_record_collection_point(self, freq_mhz: float) -> None:
        with self._result_lock:
            if not self._collection_active or self._collection_started_at is None:
                return

            now = time.time()
            self._collection_readings.append((now, freq_mhz * 1_000_000.0))

            if (now - self._collection_started_at) >= self._collection_duration_s:
                self._collection_active = False
                self._collection_done = True

    def _maybe_record_baseline_point(self, freq_mhz: float) -> None:
        with self._result_lock:
            if not self._baseline_active:
                return

            now = time.time()
            hz = freq_mhz * 1_000_000.0
            self._baseline_readings.append((now, hz))
            self._baseline_hz = hz

            if len(self._baseline_readings) >= self._baseline_required_points:
                self._baseline_active = False
                self._baseline_done = True

    def _compute_esbl_result(self) -> dict:
        with self._result_lock:
            baseline_hz = self._baseline_hz
            rows = list(self._collection_readings)
            started_at = self._collection_started_at

        if baseline_hz is None or not rows or started_at is None:
            return {
                "label": "Insufficient Data",
                "threshold_hz": self._esbl_threshold_hz,
                "baseline_hz": baseline_hz,
                "final_hz": None,
                "shift_hz": None,
                "baseline_time_s": None,
                "final_time_s": None,
                "mode": "simulation" if self.sim_mode else "experiment",
                "collection_duration_s": self._collection_duration_s,
            }

        rel_t = [t - started_at for (t, _) in rows]
        hz = [f for (_, f) in rows]

        # Final value is the last point measured during data collection.
        final_hz = hz[-1]
        shift_hz = final_hz - baseline_hz
        label = "ESBL Negative" if shift_hz > self._esbl_threshold_hz else "ESBL Positive"

        return {
            "label": label,
            "threshold_hz": self._esbl_threshold_hz,
            "baseline_hz": baseline_hz,
            "final_hz": final_hz,
            "shift_hz": shift_hz,
            "baseline_time_s": None,
            "final_time_s": rel_t[-1] if rel_t else None,
            "mode": "simulation" if self.sim_mode else "experiment",
            "collection_duration_s": self._collection_duration_s,
        }
