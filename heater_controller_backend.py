from __future__ import annotations

import os
import random
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
        sample_interval_s: float = 1.0,
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

        self._sim_mhz = 100.0

    @property
    def running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            return

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

    def _read_resonance_mhz(self) -> Optional[float]:
        if self.sim_mode:
            # Generate a stable-ish synthetic stream for UI simulation mode.
            self._sim_mhz += random.uniform(-0.008, 0.008)
            return self._sim_mhz

        try:
            result = resonance_from_scan(port=self.nanovna_port, points=101)
            return result.f_res_hz / 1_000_000.0
        except Exception:
            return None

    def _monitor_loop(self) -> None:
        while not self._stop_evt.is_set():
            freq_mhz = self._read_resonance_mhz()
            if freq_mhz is not None:
                self._send_line(f"VNA:{freq_mhz:.6f}")

            time.sleep(self.sample_interval_s)
