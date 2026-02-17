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

SIM_MODE = True


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])

        # Fullscreen + force geometry to screen size
        self._set_fullscreen(True)
        self.bind("<Escape>", lambda e: self._set_fullscreen(False))

        self.lang = "en"

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._build_frames()

        self._sim_job = None
        self._sim = {
            "temp": 22.0,
            "target": 25.0,
            "stable_got": 0,
            "stable_need": 10,
            "temp_ready": False,
            "stable_ready": False,
        }

        self.show("language")

    def _set_fullscreen(self, enabled: bool):
        try:
            self.attributes("-fullscreen", enabled)
        except Exception:
            pass

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        if enabled:
            self.geometry(f"{sw}x{sh}+0+0")
            try:
                self.attributes("-topmost", True)
            except Exception:
                pass
        else:
            try:
                self.attributes("-topmost", False)
            except Exception:
                pass
            self.geometry("1024x600")

        self.update_idletasks()

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

        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

    def show(self, key: str):
        frame = self.frames[key]
        frame.tkraise()

        # Refresh screen text on entry (fixes Arabic not applying to subsequent screens)
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception:
                pass

        if SIM_MODE:
            self._start_sim_for_screen(key)

    def set_language(self, lang: str):
        self.lang = lang

    def reset_to_start(self):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._sim.update(
            temp=22.0,
            target=25.0,
            stable_got=0,
            stable_need=10,
            temp_ready=False,
            stable_ready=False,
        )
        self.show("language")

    # ---------- Flow actions ----------
    def go_from_language(self):
        self.show("welcome")

    def go_from_welcome(self):
        self.show("preheat")

    def confirm_preheat_next(self):
        self.show("load_sample")

    def confirm_sample_loaded(self):
        self.show("device_check_1")

    def confirm_device_check_baseline_start(self):
        self.show("baseline")

    def confirm_baseline_next(self):
        self.show("load_antibiotic")

    def confirm_antibiotic_loaded(self):
        self.show("device_check_2")

    def confirm_device_check_collection_start(self):
        self.show("data_collection")

    def confirm_data_collection_next(self):
        self.show("result")

    # ---------- Simulation loops ----------
    def _start_sim_for_screen(self, key: str):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        if key == "preheat":
            self._sim.update(temp=22.0, stable_got=0, temp_ready=False, stable_ready=False)
            self._tick_preheat_sim()
        elif key == "baseline":
            self._sim.update(stable_got=0, stable_ready=False)
            self._tick_baseline_sim()
        elif key == "data_collection":
            self.frames["data_collection"].simulate_progress()

    def _tick_preheat_sim(self):
        self._sim["temp"] = min(self._sim["target"], self._sim["temp"] + 0.4)
        self._sim["temp_ready"] = abs(self._sim["temp"] - self._sim["target"]) <= 0.2

        if self._sim["stable_got"] < self._sim["stable_need"]:
            self._sim["stable_got"] += 1
        self._sim["stable_ready"] = self._sim["stable_got"] >= self._sim["stable_need"]

        self.frames["preheat"].set_state(
            current_c=self._sim["temp"],
            target_c=self._sim["target"],
            stable_got=self._sim["stable_got"],
            stable_need=self._sim["stable_need"],
            temp_ready=self._sim["temp_ready"],
            stable_ready=self._sim["stable_ready"],
        )

        self._sim_job = self.after(300, self._tick_preheat_sim)

    def _tick_baseline_sim(self):
        if self._sim["stable_got"] < self._sim["stable_need"]:
            self._sim["stable_got"] += 1
        self._sim["stable_ready"] = self._sim["stable_got"] >= self._sim["stable_need"]

        self.frames["baseline"].set_stability(
            self._sim["stable_got"],
            self._sim["stable_need"],
            self._sim["stable_ready"],
        )

        self._sim_job = self.after(300, self._tick_baseline_sim)
