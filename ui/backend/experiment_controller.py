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

@dataclass
class ControllerState:
    step: str = "IDLE"
    current_temp_c: Optional[float] = None
    resonance_hz: Optional[float] = None
    stable_got: int = 0
    stable_need: int = 10
    temp_ready: bool = False
    stable_ready: bool = False

class ExperimentController:
    """
    Steps:
      PREHEAT (heating + stability checking simultaneously; UI NEXT disabled until ready)
      LOAD_PROCESSED_SAMPLE (user confirm)
      DEVICE_CHECK_BASELINE (user confirm -> start baseline collection)
      BASELINE_COLLECT (stability-gated; ends when stable)
      LOAD_ANTIBIOTIC (user confirm)
      DONE
    """
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

    def _poll_once(self):
        st = self.arduino.status()
        if st:
            self.state.current_temp_c = st.get("t2")

        freq = self.vna.latest_resonance_hz()
        if freq is not None:
            self.state.resonance_hz = freq

        # temp ready?
        if self.state.current_temp_c is None:
            self.state.temp_ready = False
        else:
            self.state.temp_ready = abs(self.state.current_temp_c - self.cfg.target_temp_c) <= self.cfg.temp_deadband_c

        self._emit_state()

    def _run(self):
        # Start heating immediately
        self._set_step("PREHEAT")
        try:
            self.arduino.start(self.cfg.target_temp_c)
        except Exception:
            return

        # PREHEAT: simultaneously check temperature AND stability (anchor-based)
        self._stable.reset()
        self.state.stable_ready = False

        while not self._stop_evt.is_set():
            self._poll_once()

            if self.state.resonance_hz is not None:
                ok = self._stable.update(self.state.resonance_hz)
                got, need = self._stable.progress()
                self.state.stable_got = got
                self.state.stable_need = need
                self.state.stable_ready = ok
                self._emit_state()

            # We don't auto-advance here; UI will enable NEXT only when:
            # temp_ready AND stable_ready, then user presses NEXT.
            if self._wait_confirm("preheat_next"):
                break

            time.sleep(0.4)

        if self._stop_evt.is_set():
            return

        # LOAD PROCESSED SAMPLE
        self._set_step("LOAD_PROCESSED_SAMPLE")
        if not self._wait_confirm("sample_loaded"):
            return

        # DEVICE CHECK (baseline)
        self._set_step("DEVICE_CHECK_BASELINE")
        if not self._wait_confirm("baseline_start"):
            return

        # BASELINE COLLECT: no timer; ends when stability met
        self._set_step("BASELINE_COLLECT")
        self._stable.reset()
        self.state.stable_ready = False
        self.state.stable_got = 0
        self.state.stable_need = self.cfg.stable_n

        while not self._stop_evt.is_set():
            self._poll_once()
            if self.state.resonance_hz is not None:
                ok = self._stable.update(self.state.resonance_hz)
                got, need = self._stable.progress()
                self.state.stable_got = got
                self.state.stable_need = need
                self.state.stable_ready = ok
                self._emit_state()
                if ok:
                    break
            time.sleep(0.4)

        if self._stop_evt.is_set():
            return

        # LOAD ANTIBIOTIC
        self._set_step("LOAD_ANTIBIOTIC")
        if not self._wait_confirm("antibiotic_loaded"):
            return

        self._set_step("DONE")
        self._emit_state()
