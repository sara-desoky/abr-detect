# ui/backend/experiment_controller.py
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

from ui.backend.stability import StabilityChecker

@dataclass
class ControllerConfig:
    target_temp_c: float = 25.0
    temp_deadband_c: float = 0.2
    stable_n: int = 10
    stable_thresh_mhz: float = 0.06
    baseline_seconds: int = 7 * 60

@dataclass
class ControllerState:
    step: str = "IDLE"
    current_temp_c: Optional[float] = None
    resonance_hz: Optional[float] = None
    stable_got: int = 0
    stable_need: int = 10

class ExperimentController:
    def __init__(
        self,
        arduino,
        vna_reader,
        config: ControllerConfig,
        on_state: Callable[[ControllerState], None],
        on_step_change: Callable[[str], None],
    ):
        self.arduino = arduino
        self.vna = vna_reader
        self.cfg = config

        self.on_state = on_state
        self.on_step_change = on_step_change

        self.state = ControllerState(stable_need=self.cfg.stable_n)
        self._stable = StabilityChecker(self.cfg.stable_n, self.cfg.stable_thresh_mhz)

        self._stop_evt = threading.Event()
        self._confirm_lock = threading.Lock()
        self._confirm_flag: Optional[str] = None

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._stop_evt.set()
        try:
            self.arduino.stop()
        except Exception:
            pass

    def user_confirm(self, name: str):
        with self._confirm_lock:
            self._confirm_flag = name

    def _wait_confirm(self, name: str) -> bool:
        while not self._stop_evt.is_set():
            with self._confirm_lock:
                if self._confirm_flag == name:
                    self._confirm_flag = None
                    return True
            time.sleep(0.1)
        return False

    def _emit_state(self):
        self.on_state(self.state)

    def _set_step(self, step: str):
        self.state.step = step
        self.on_step_change(step)

    def _run(self):
        # PREHEAT
        self._set_step("PREHEAT")
        try:
            self.arduino.start(self.cfg.target_temp_c)
        except Exception:
            return

        # WAIT_STABLE_PREBASELINE
        self._set_step("WAIT_STABLE_PREBASELINE")
        self._stable.reset()

        while not self._stop_evt.is_set():
            st = self.arduino.status()
            if st:
                self.state.current_temp_c = st.get("t2")

            freq = self.vna.latest_resonance_hz()
            if freq is not None:
                self.state.resonance_hz = freq

            near_target = (
                self.state.current_temp_c is not None
                and abs(self.state.current_temp_c - self.cfg.target_temp_c) <= self.cfg.temp_deadband_c
            )

            if near_target and freq is not None:
                ok = self._stable.update(freq)
                got, need = self._stable.progress()
                self.state.stable_got = got
                self.state.stable_need = need
                self._emit_state()
                if ok:
                    break
            else:
                self._emit_state()

            time.sleep(0.5)

        if self._stop_evt.is_set():
            return

        # LOAD_PROCESSED_SAMPLE
        self._set_step("LOAD_PROCESSED_SAMPLE")
        if not self._wait_confirm("sample_loaded"):
            return

        # BASELINE_PROGRESS (time only)
        self._set_step("BASELINE_PROGRESS")
        t0 = time.time()
        while not self._stop_evt.is_set():
            if (time.time() - t0) >= self.cfg.baseline_seconds:
                break
            # still update resonance if available
            freq = self.vna.latest_resonance_hz()
            if freq is not None:
                self.state.resonance_hz = freq
            self._emit_state()
            time.sleep(0.5)

        if self._stop_evt.is_set():
            return

        # WAIT_STABLE_PREPENG
        self._set_step("WAIT_STABLE_PREPENG")
        self._stable.reset()

        while not self._stop_evt.is_set():
            freq = self.vna.latest_resonance_hz()
            if freq is not None:
                self.state.resonance_hz = freq
                ok = self._stable.update(freq)
                got, need = self._stable.progress()
                self.state.stable_got = got
                self.state.stable_need = need
                self._emit_state()
                if ok:
                    break
            else:
                self._emit_state()
            time.sleep(0.5)

        if self._stop_evt.is_set():
            return

        # ADD_PENG (we show baseline_ready screen first in AppUI mapping)
        self._set_step("ADD_PENG")
        if not self._wait_confirm("peng_added"):
            return

        # DONE
        self._set_step("DONE")
        self._emit_state()
