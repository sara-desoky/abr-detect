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

from ui.backend.experiment_controller import (
    ExperimentController,
    ControllerConfig,
    ControllerState,
)

SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg=COLORS["bg"])

        # ✅ FULLSCREEN
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.lang = "en"

        self.cfg = ControllerConfig(
            target_temp_c=25.0,
            temp_deadband_c=0.2,
            stable_n=10,
            stable_thresh_mhz=0.06,
        )

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self._build_frames()

        self.controller = None
        self.show("language")

    def _build_frames(self):

        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)
        self.frames["preheat"] = PreheatScreen(self.container, self)
        self.frames["load_sample"] = LoadProcessedSampleScreen(self.container, self)
        self.frames["device_check_1"] = DeviceCheckScreen(self.container, self, phase="baseline")
        self.frames["baseline"] = BaselineMeasurementScreen(self.container, self)
        self.frames["load_antibiotic"] = LoadAntibioticScreen(self.container, self)
        self.frames["device_check_2"] = DeviceCheckScreen(self.container, self, phase="collection")
        self.frames["data_collection"] = DataCollectionScreen(self.container, self)
        self.frames["result"] = ResultScreen(self.container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show(self, key):
        self.frames[key].tkraise()

    # Temporary SIM FLOW for now (so you can test UI)
    def simulate_next(self, current):
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

        idx = flow.index(current)
        if idx < len(flow) - 1:
            self.show(flow[idx + 1])
