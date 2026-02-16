# ui/app_ui.py
import tkinter as tk
import time
import threading

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

# ✅ Toggle this to test with NO Arduino + NO VNA
SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])
        self.geometry("1024x600")

        # app state
        self.lang = "en"

        # ---- experiment config ----
        self.cfg = ControllerConfig(
            target_temp_c=25.0,
            temp_deadband_c=0.2,
            stable_n=10,
            stable_thresh_mhz=0.06,
            baseline_seconds=7 * 60,   # 7 minutes
        )

        # ---- real hardware settings (only used when SIM_MODE=False) ----
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

        # Start screen
        self.show("language")  # your desired first screen

    # ---------------- UI routing ----------------
    def _build_frames(self):
        # existing screens
        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)

        # new flow screens
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

        # Start backend once we enter preheat (first screen af
