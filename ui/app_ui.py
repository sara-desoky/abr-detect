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

SIM_MODE = True  # <- keep this True for testing


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])
        self.geometry("1024x600")

        self.lang = "en"
        self.SIM_MODE = SIM_MODE  # expose to screens

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_frames()

        self.show("language")

    # ---------------- Build Screens ----------------
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

    # ---------------- Screen Navigation ----------------
    def show(self, key: str):
        self.frames[key].tkraise()

    # ---------------- Button Callbacks ----------------
    def confirm_preheat_next(self):
        self.show("load_processed_sample")

    def confirm_sample_loaded(self):
        self.show("load_antibiotic")

    def confirm_antibiotic_loaded(self):
        self.show("done")

    def stop_all(self):
        self.show("welcome")
