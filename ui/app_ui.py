# ui/app_ui.py
import tkinter as tk

from ui.config import COLORS

from ui.screens.welcome import WelcomeScreen
from ui.screens.language_select import LanguageSelectScreen

from ui.screens.preheat import PreheatScreen
from ui.screens.wait_stability import WaitStabilityScreen
from ui.screens.load_processed_sample import LoadProcessedSampleScreen
from ui.screens.baseline_progress import BaselineProgressScreen
from ui.screens.baseline_ready import BaselineReadyScreen
from ui.screens.add_peng import AddPenGScreen
from ui.screens.done import DoneScreen

from ui.backend.experiment_controller import (
    ExperimentController,
    ControllerConfig,
    ControllerState,
)

# Toggle to test with NO Arduino + NO VNA
SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])
        self.geometry("1024x600")

        # App-wide state
        self.lang = "en"

        # Experiment config
        self.cfg = ControllerConfig(
            target_temp_c=25.0,
            temp_deadband_c=0.2,
            stable_n=10,
            stable_thresh_mhz=0.06,
            baseline_seconds=7 * 60,  # 7 minutes
        )

        # Real hardware settings (only used when SIM_MODE=False)
        self.arduino_port = "/dev/ttyACM0"
        self.result_file_path = "/home/pi/ABRDetect/Run7/result_Run7.txt"

        # UI container
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        self._build_frames()

        self.controller: ExperimentController | None = None

        # Start screen (your desired first screen)
        self.show("language")

    # ---------------- UI routing ----------------
    def _build_frames(self):
        # Existing screens
        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)

        # Flow screens
        self.frames["preheat"] = PreheatScreen(self.container, self)

        self.frames["wait_stable_prebaseline"] = WaitStabilityScreen(
            self.container, self, title_key="prebaseline"
        )

        self.frames["load_processed_sample"] = LoadProcessedSampleScreen(self.container, self)

        self.frames["baseline_progress"] = BaselineProgressScreen(self.container, self)

        self.frames["wait_stable_preg"] = WaitStabilityScreen(
            self.container, self, title_key="preg"
        )

        self.frames["baseline_ready"] = BaselineReadyScreen(self.container, self)
        self.frames["add_peng"] = AddPenGScreen(self.container, self)
        self.frames["done"] = DoneScreen(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show(self, key: str):
        self.frames[key].tkraise()

        # Start backend once we enter preheat
        if key == "preheat":
            self._ensure_controller_running()

    # ---------------- Controller setup ----------------
    def _ensure_controller_running(self):
        if self.controller is not None:
            return

        if SIM_MODE:
            from ui.backend.sim_devices import SimArduino, SimVNA
            arduino = SimArduino(start_temp=22.0)
            vna = SimVNA()
        else:
            from ui.backend.arduino_serial import ArduinoSerial
            from ui.backend.vna_reader_file import VNAReaderFile
            arduino = ArduinoSerial(self.arduino_port, baud=115200)
            vna = VNAReaderFile(self.result_file_path)

        self.controller = ExperimentController(
            arduino=arduino,
            vna_reader=vna,
            config=self.cfg,
            on_state=lambda s: self.after(0, lambda: self._on_state(s)),
            on_step_change=lambda step: self.after(0, lambda: self._on_step(step)),
        )
        self.controller.start()

    # ---------------- Controller callbacks ----------------
    def _on_step(self, step: str):
        """
        Controller steps -> UI screens
        """
        if step == "PREHEAT":
            self.show("preheat")

        elif step == "WAIT_STABLE_PREBASELINE":
            self.show("wait_stable_prebaseline")

        elif step == "LOAD_PROCESSED_SAMPLE":
            self.show("load_processed_sample")

        elif step == "BASELINE_PROGRESS":
            self.show("baseline_progress")
            bp: BaselineProgressScreen = self.frames["baseline_progress"]  # type: ignore
            bp.start_countdown(self.cfg.baseline_seconds)

        elif step == "WAIT_STABLE_PREPENG":
            self.show("wait_stable_preg")

        elif step == "ADD_PENG":
            self.show("baseline_ready")

        elif step == "DONE":
            self.show("done")

    def _on_state(self, state: ControllerState):
        # Preheat temp
        preheat: PreheatScreen = self.frames["preheat"]  # type: ignore
        preheat.set_temp(state.current_temp_c, self.cfg.target_temp_c)

        # Stability wait screens
        ws1: WaitStabilityScreen = self.frames["wait_stable_prebaseline"]  # type: ignore
        ws2: WaitStabilityScreen = self.frames["wait_stable_preg"]  # type: ignore
        ws1.set_freq(state.resonance_hz)
        ws2.set_freq(state.resonance_hz)
        ws1.set_progress(state.stable_got, state.stable_need, self.cfg.stable_thresh_mhz)
        ws2.set_progress(state.stable_got, state.stable_need, self.cfg.stable_thresh_mhz)

        # Baseline progress screen (optional frequency display)
        bp: BaselineProgressScreen = self.frames["baseline_progress"]  # type: ignore
        bp.set_freq(state.resonance_hz)

    # ---------------- UI buttons -> controller signals ----------------
    def confirm_sample_loaded(self):
        if self.controller:
            self.controller.user_confirm("sample_loaded")

    def confirm_peng_added(self):
        if self.controller:
            self.controller.user_confirm("peng_added")

    # ---------------- Required by PreheatScreen STOP button ----------------
    def stop_all(self):
        if self.controller:
            self.controller.stop()
            self.controller = None
        # return to welcome or language; your choice
        self.show("welcome")
