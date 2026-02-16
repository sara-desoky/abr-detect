# ui/app_ui.py
import tkinter as tk
from ui.config import COLORS

from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen

from ui.screens.setup_pdms import SetupPDMSScreen
from ui.screens.preheat import PreheatScreen
from ui.screens.load_processed_sample import LoadProcessedSampleScreen
from ui.screens.device_check import DeviceCheckScreen
from ui.screens.baseline_progress import BaselineProgressScreen
from ui.screens.load_antibiotic import LoadAntibioticScreen
from ui.screens.done import DoneScreen

from ui.backend.experiment_controller import (
    ExperimentController,
    ControllerConfig,
    ControllerState,
)

SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])
        self.geometry("1024x600")

        self.lang = "en"

        # IMPORTANT: no baseline_seconds here anymore
        self.cfg = ControllerConfig(
            target_temp_c=25.0,
            temp_deadband_c=0.2,
            stable_n=10,
            stable_thresh_mhz=0.06,
        )

        self.arduino_port = "/dev/ttyACM0"
        self.result_file_path = "/home/pi/ABRDetect/Run7/result_Run7.txt"

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        self.controller: ExperimentController | None = None

        self._build_frames()
        self.show("language")

    def _build_frames(self):
        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)

        # new flow (after welcome)
        self.frames["setup_pdms"] = SetupPDMSScreen(self.container, self)
        self.frames["preheat"] = PreheatScreen(self.container, self)
        self.frames["load_processed_sample"] = LoadProcessedSampleScreen(self.container, self)
        self.frames["device_check"] = DeviceCheckScreen(self.container, self)
        self.frames["baseline_progress"] = BaselineProgressScreen(self.container, self)
        self.frames["load_antibiotic"] = LoadAntibioticScreen(self.container, self)
        self.frames["done"] = DoneScreen(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show(self, key: str):
        self.frames[key].tkraise()
        if key == "preheat":
            self._ensure_controller_running()

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

    def _on_step(self, step: str):
        if step == "PREHEAT":
            self.show("preheat")
        elif step == "LOAD_PROCESSED_SAMPLE":
            self.show("load_processed_sample")
        elif step == "DEVICE_CHECK_BASELINE":
            self.show("device_check")
        elif step == "BASELINE_COLLECT":
            self.show("baseline_progress")
        elif step == "LOAD_ANTIBIOTIC":
            self.show("load_antibiotic")
        elif step == "DONE":
            self.show("done")

    def _on_state(self, state: ControllerState):
        # PREHEAT updates
        pre: PreheatScreen = self.frames["preheat"]  # type: ignore
        pre.set_temp(state.current_temp_c, self.cfg.target_temp_c, state.temp_ready)
        pre.set_stability(state.stable_got, state.stable_need, state.stable_ready)

        # BASELINE updates
        bp: BaselineProgressScreen = self.frames["baseline_progress"]  # type: ignore
        bp.set_freq(state.resonance_hz)
        bp.set_stability(state.stable_got, state.stable_need, state.stable_ready)

    # --- UI -> controller confirms ---
    def confirm_preheat_next(self):
        if self.controller:
            self.controller.user_confirm("preheat_next")

    def confirm_sample_loaded(self):
        if self.controller:
            self.controller.user_confirm("sample_loaded")

    def confirm_baseline_start(self):
        if self.controller:
            self.controller.user_confirm("baseline_start")

    def confirm_antibiotic_loaded(self):
        if self.controller:
            self.controller.user_confirm("antibiotic_loaded")

    def stop_all(self):
        if self.controller:
            self.controller.stop()
            self.controller = None
        self.show("welcome")
