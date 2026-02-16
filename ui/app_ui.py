# ui/app_ui.py
import tkinter as tk

from ui.config import COLORS

from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen
from ui.screens.setup_pdms import SetupPDMSScreen
from ui.screens.preheat import PreheatScreen
from ui.screens.load_processed_sample import LoadProcessedSampleScreen
from ui.screens.device_check import DeviceCheckScreen
from ui.screens.baseline_measurement import BaselineMeasurementScreen
from ui.screens.load_antibiotic import LoadAntibioticScreen
from ui.screens.data_collection import DataCollectionScreen
from ui.screens.result_screen import ResultScreen


# Option A = UI-only simulation (no Arduino, no VNA, no backend)
SIM_MODE = True


class AppUI(tk.Tk):
    """
    UI Flow (Option A):
      language -> welcome -> setup_pdms -> preheat -> load_sample
      -> device_check_1 -> baseline -> load_antibiotic
      -> device_check_2 -> data_collection -> result
    """
    def __init__(self):
        super().__init__()

        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])

        # Fullscreen kiosk mode on Pi
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # app state
        self.lang = "en"

        # UI container
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        self._build_frames()

        # Start screen
        self.show("language")

    def _build_frames(self):
        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)

        self.frames["setup_pdms"] = SetupPDMSScreen(self.container, self)
        self.frames["preheat"] = PreheatScreen(self.container, self)

        self.frames["load_sample"] = LoadProcessedSampleScreen(self.container, self)

        self.frames["device_check_1"] = DeviceCheckScreen(self.container, self)
        self.frames["baseline"] = BaselineMeasurementScreen(self.container, self)

        self.frames["load_antibiotic"] = LoadAntibioticScreen(self.container, self)

        self.frames["device_check_2"] = DeviceCheckScreen(self.container, self)
        self.frames["data_collection"] = DataCollectionScreen(self.container, self)
        self.frames["result"] = ResultScreen(self.container, self)

        # configure the 2 device-check screens (same class, different text + next)
        dc1: DeviceCheckScreen = self.frames["device_check_1"]  # type: ignore
        dc2: DeviceCheckScreen = self.frames["device_check_2"]  # type: ignore
        dc1.configure_phase("baseline")
        dc2.configure_phase("collection")

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show(self, key: str):
        self.frames[key].tkraise()

        # When a screen needs to kick off a simulated “progress”, do it here.
        if SIM_MODE:
            if key == "preheat":
                pre: PreheatScreen = self.frames["preheat"]  # type: ignore
                pre.start_sim()
            elif key == "baseline":
                bl: BaselineMeasurementScreen = self.frames["baseline"]  # type: ignore
                bl.start_sim()
            elif key == "data_collection":
                dc: DataCollectionScreen = self.frames["data_collection"]  # type: ignore
                dc.start_sim()

    # ---------- Option A: simple flow helper ----------
    def simulate_next(self, current_key: str):
        flow = [
            "setup_pdms",
            "preheat",
            "load_sample",
            "device_check_1",
            "baseline",
            "load_antibiotic",
            "device_check_2",
            "data_collection",
            "result",
        ]
        if current_key not in flow:
            return
        idx = flow.index(current_key)
        if idx < len(flow) - 1:
            self.show(flow[idx + 1])

    # ---------- callbacks used by screens ----------
    def on_language_selected(self, lang: str):
        self.lang = lang
        self.show("welcome")

    def go_from_welcome(self):
        self.show("setup_pdms")

    def confirm_pdms_setup(self):
        self.show("preheat")

    def confirm_preheat_next(self):
        self.simulate_next("preheat")

    def confirm_sample_loaded(self):
        self.simulate_next("load_sample")

    def confirm_antibiotic_loaded(self):
        self.simulate_next("load_antibiotic")

    def finish(self):
        # End of flow: go back to language select
        self.show("language")
