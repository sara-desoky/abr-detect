# ui/app_ui.py
import tkinter as tk
from ui.config import COLORS

from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen
from ui.screens.preheat import PreheatScreen
from ui.screens.load_processed_sample import LoadProcessedSampleScreen
from ui.screens.device_check import DeviceCheckScreen
from ui.screens.baseline_measurement import BaselineMeasurementScreen
from ui.screens.load_antibiotic import LoadAntibioticScreen
from ui.screens.data_collection import DataCollectionScreen
from ui.screens.result_screen import ResultScreen


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg=COLORS["bg"])

        # ✅ FULLSCREEN
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.lang = "en"

        # Main container
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_frames()

        self.show("language")

    # -----------------------------
    # Build All Screens
    # -----------------------------
    def _build_frames(self):

        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)
        self.frames["preheat"] = PreheatScreen(self.container, self)
        self.frames["load_sample"] = LoadProcessedSampleScreen(self.container, self)

        # TWO device checks
        self.frames["device_check_1"] = DeviceCheckScreen(self.container, self)
        self.frames["device_check_2"] = DeviceCheckScreen(self.container, self)

        self.frames["baseline"] = BaselineMeasurementScreen(self.container, self)
        self.frames["load_antibiotic"] = LoadAntibioticScreen(self.container, self)
        self.frames["data_collection"] = DataCollectionScreen(self.container, self)
        self.frames["result"] = ResultScreen(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    # -----------------------------
    # Screen Routing
    # -----------------------------
    def show(self, key):
        frame = self.frames[key]

        # Configure device check screens dynamically
        if key == "device_check_1":
            frame.configure_phase("baseline")

        elif key == "device_check_2":
            frame.configure_phase("collection")

        frame.tkraise()

    # -----------------------------
    # SIMULATION FLOW
    # -----------------------------
    def simulate_next(self, current):
        """
        Manual UI simulation flow (no backend)
        """

        flow = [
            "preheat",
            "load_sample",
            "device_check_1",
            "baseline",
            "load_antibiotic",
            "device_check_2",
            "data_collection",
            "result",
        ]

        if current not in flow:
            return

        idx = flow.index(current)
        if idx < len(flow) - 1:
            self.show(flow[idx + 1])
