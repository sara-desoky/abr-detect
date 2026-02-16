# ui/app_ui.py
import tkinter as tk

from ui.config import COLORS

from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen
from ui.screens.setup_pdms import SetupPDMSScreen
from ui.screens.preheat import PreheatScreen
from ui.screens.load_processed_sample import LoadProcessedSampleScreen
from ui.screens.load_antibiotic import LoadAntibioticScreen
from ui.screens.done import DoneScreen

from ui.backend.experiment_controller import (
    ExperimentController,
    ControllerConfig,
    ControllerState,
)

# ---------------------------------------------------
# Toggle simulation mode
# ---------------------------------------------------
SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])
        self.geometry("1024x600")

        self.lang = "en"

        # ---------------------------------------------------
        # FAST SIM SETTINGS (Option A)
        # ---------------------------------------------------
        if SIM_MODE:
            self.cfg = ControllerConfig(
                target_temp_c=25.0,
                temp_deadband_c=5.0,      # very wide for sim
                stable_n=2,               # only 2 stable samples needed
                stable_thresh_mhz=5.0,    # huge threshold for sim
            )
        else:
            self.cfg = ControllerConfig(
                target_temp_c=25.0,
                temp_deadband_c=0.2,
                stable_n=10,
                stable_thresh_mhz=0.06,
            )

        self.arduino_port = "/dev/ttyACM0"
        self.result_file_path = "/home/pi/ABRDetect/Run7/result_Run7.txt"

        # ---------------------------------------------------
        # Container
        # ---------------------------------------------------
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        self._build_frames()

        self.controller: ExperimentController | None = None

        self.show("language")

    # ---------------------------------------------------
    # Build Screens
    # ---------------------------------------------------
    def _build_frames(self):

        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)
        self.frames["setup_pdms"] = SetupPDMSScreen(self.container, self)
        self.frames["preheat"] = PreheatScreen(self.container, self)
        self.frames["load_processed_sample"] = LoadProcessedSampleScreen(self.container, self)
        self.frames["load_antibiotic"] = LoadAntibioticScreen(self.container, self)
        self.frames["done"] = DoneScreen(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    # ---------------------------------------------------
    # Screen Navigation
    # ---------------------------------------------------
    def show(self, key: str):
        self.frames[key].tkraise()

        if key == "preheat":
            self._ensure_controller_running()

    # ---------------------------------------------------
    # Start Controller
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # Controller → UI Step Changes
    # ---------------------------------------------------
    def _on_step(self, step: str):

        if step == "PREHEAT":
            self.show("preheat")

        elif step == "LOAD_PROCESSED_SAMPLE":
            self.show("load_processed_sample")

        elif step == "LOAD_ANTIBIOTIC":
            self.show("load_antibiotic")

        elif step == "DONE":
            self.show("done")

    # ---------------------------------------------------
    # Controller → UI State Updates
    # ---------------------------------------------------
    def _on_state(self, state: ControllerState):

        preheat: PreheatScreen = self.frames["preheat"]  # type: ignore

        preheat.set_temp(state.current_temp_c, self.cfg.target_temp_c)
        preheat.set_stability(state.stable_got, state.stable_need)

        # Enable NEXT only when BOTH are ready
        if state.temp_ready and state.stable_ready:
            preheat.enable_next()
        else:
            preheat.disable_next()

    # ---------------------------------------------------
    # Button → Controller Signals
    # ---------------------------------------------------
    def confirm_preheat_next(self):
        if self.controller:
            self.controller.user_confirm("preheat_next")

    def confirm_sample_loaded(self):
        if self.controller:
            self.controller.user_confirm("sample_loaded")

    def confirm_antibiotic_loaded(self):
        if self.controller:
            self.controller.user_confirm("antibiotic_loaded")

    # ---------------------------------------------------
    # Emergency Stop
    # ---------------------------------------------------
    def stop_all(self):
        if self.controller:
            self.controller.stop()
            self.controller = None
        self.show("welcome")
