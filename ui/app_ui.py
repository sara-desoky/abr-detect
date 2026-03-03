# ui/app_ui.py
import os
import tkinter as tk

from ui.config import COLORS
from ui.rtl import rtl
from heater_controller_backend import HeaterExperimentController

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

SIM_MODE = os.getenv("ABR_SIM_MODE", "1") not in {"0", "false", "False"}


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.configure(bg=COLORS["bg"])

        self.lang = "en"
        self.experiment_controller = HeaterExperimentController(sim_mode=SIM_MODE)

        # ---- Fullscreen state ----
        self._is_fullscreen = True
        self._apply_fullscreen(True)

        # ESC: immediate emergency exit
        self.bind("<Escape>", lambda e: self.safe_quit())

        # Emergency exit (always works)
        self.bind("<Control-q>", lambda e: self.safe_quit())
        self.bind("<Control-Q>", lambda e: self.safe_quit())

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._current_screen = None
        self._build_frames()
        self._build_language_toggle()
        self._build_cancel_button()

        # ---- Simulation state ----
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

    # ---------------- Fullscreen controls ----------------
    def _apply_fullscreen(self, enabled: bool):
        self._is_fullscreen = enabled
        try:
            self.attributes("-fullscreen", enabled)
        except Exception:
            pass

        # Force the window size to the display size
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

        # DO NOT call update() here (can freeze on Pi sometimes)
        self.update_idletasks()

    def safe_quit(self):
        # Cancel any sim jobs + close app
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None
        try:
            self.experiment_controller.stop()
        except Exception:
            pass
        self.destroy()

    def finish_and_quit(self):
        # Explicit end-of-test action from Result screen.
        try:
            self.experiment_controller.stop()
        except Exception:
            pass
        self.destroy()

    # ---------------- Screen building / navigation ----------------
    def _build_frames(self):
        self.frames["language"] = LanguageSelectScreen(self.container, self)
        self.frames["welcome"] = WelcomeScreen(self.container, self)
        self.frames["setup_pdms"] = SetupPDMSScreen(self.container, self)

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

    def _build_language_toggle(self):
        self.lang_toggle_btn = tk.Button(
            self,
            text="",
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            bd=1,
            padx=12,
            pady=6,
            command=self.toggle_language,
        )
        # Consistent position across all screens.
        self.lang_toggle_btn.place(x=16, y=16)
        self._update_language_toggle_label()

    def _build_cancel_button(self):
        self.cancel_btn = tk.Button(
            self,
            text="Cancel Experiment",
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["text"],
            activebackground=COLORS["btn_disabled_bg"],
            activeforeground=COLORS["text"],
            bd=1,
            padx=8,
            pady=4,
            command=self._on_cancel_experiment_clicked,
        )
        self.cancel_btn.place(relx=1.0, x=-16, y=16, anchor="ne")
        self._update_cancel_button()

    def show(self, key: str):
        self._current_screen = key
        frame = self.frames[key]
        frame.tkraise()

        # Let screens refresh text/layout when shown (for Arabic switching)
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception:
                pass

        if SIM_MODE:
            self._start_sim_for_screen(key)

        self._update_language_toggle_label()
        self._update_cancel_button()

        # Hide the global language toggle on the language selection screen
        # since that screen already has dedicated language options.
        if key == "language":
            self.lang_toggle_btn.place_forget()
        else:
            self.lang_toggle_btn.place(x=16, y=16)
            self.lang_toggle_btn.lift()
        self.cancel_btn.lift()

    # ---------------- Language / resets ----------------
    def set_language(self, lang: str):
        self.lang = lang
        self._update_language_toggle_label()

    def toggle_language(self):
        self.lang = "ar" if self.lang == "en" else "en"
        self._update_language_toggle_label()
        self._update_cancel_button()

        if not self._current_screen:
            return

        frame = self.frames.get(self._current_screen)
        if frame is not None and hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception:
                pass

    def _update_language_toggle_label(self):
        # Show the language that pressing the button will switch to.
        if self.lang == "en":
            self.lang_toggle_btn.config(text=rtl("العربية"))
        else:
            self.lang_toggle_btn.config(text="English")

    def _update_cancel_button(self):
        show_on = {
            "setup_pdms",
            "preheat",
            "load_sample",
            "device_check_1",
            "baseline",
            "load_antibiotic",
            "device_check_2",
            "data_collection",
        }
        if self._current_screen in show_on:
            if self.lang == "ar":
                self.cancel_btn.config(text=rtl("إلغاء الاختبار"))
            else:
                self.cancel_btn.config(text="Cancel Experiment")
            self.cancel_btn.place(relx=1.0, x=-16, y=16, anchor="ne")
        else:
            self.cancel_btn.place_forget()

    def _on_cancel_experiment_clicked(self):
        if not self._confirm_cancel_dialog():
            return
        self.cancel_and_reset_experiment()

    def _confirm_cancel_dialog(self) -> bool:
        dialog = tk.Toplevel(self)
        if self.lang == "ar":
            dialog.title(rtl("إلغاء الاختبار؟"))
        else:
            dialog.title("Cancel Experiment?")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        accepted = {"value": False}

        if self.lang == "ar":
            title_text = rtl("إلغاء الاختبار؟")
            msg_text = rtl("سيؤدي هذا إلى إيقاف كل القياسات وإعادة ضبط الجهاز. سيتم فقدان أي بيانات تم جمعها.")
            keep_text = rtl("متابعة الاختبار")
            cancel_text = rtl("إلغاء وإعادة ضبط")
            msg_justify = "right"
            msg_font = ("Noto Naskh Arabic", 14)
            title_font = ("Noto Naskh Arabic", 20, "bold")
        else:
            title_text = "Cancel Experiment?"
            msg_text = "This will stop all measurements and reset the device. Any collected data will be lost."
            keep_text = "Continue Experiment"
            cancel_text = "Cancel & Reset"
            msg_justify = "left"
            msg_font = ("Arial", 14)
            title_font = ("Times New Roman", 20, "bold")

        title_lbl = tk.Label(
            dialog,
            text=title_text,
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=title_font,
        )
        title_lbl.pack(padx=24, pady=(20, 12))

        msg_lbl = tk.Label(
            dialog,
            text=msg_text,
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify=msg_justify,
            wraplength=560,
            font=msg_font,
        )
        msg_lbl.pack(padx=24, pady=(0, 18))

        btn_row = tk.Frame(dialog, bg=COLORS["bg"])
        btn_row.pack(pady=(0, 20))

        keep_btn = tk.Button(
            btn_row,
            text=keep_text,
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["text"],
            padx=12,
            pady=6,
            command=dialog.destroy,
        )
        keep_btn.grid(row=0, column=0, padx=10)

        cancel_btn = tk.Button(
            btn_row,
            text=cancel_text,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            padx=12,
            pady=6,
            command=lambda: (accepted.__setitem__("value", True), dialog.destroy()),
        )
        cancel_btn.grid(row=0, column=1, padx=10)

        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        self.wait_window(dialog)
        return accepted["value"]
    def cancel_and_reset_experiment(self):
        # Stop app-level simulation loop.
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        # Stop per-screen measurement/simulation loops if they exist.
        for frame in self.frames.values():
            job = getattr(frame, "_sim_job", None)
            if job is not None:
                try:
                    frame.after_cancel(job)
                except Exception:
                    pass
                try:
                    frame._sim_job = None
                except Exception:
                    pass
            if hasattr(frame, "_pct"):
                try:
                    frame._pct = 0
                except Exception:
                    pass
            if hasattr(frame, "_sim_step"):
                try:
                    frame._sim_step = 0
                except Exception:
                    pass

        # Reset internal state values.
        self._sim.update(
            temp=22.0,
            target=25.0,
            stable_got=0,
            stable_need=10,
            temp_ready=False,
            stable_ready=False,
        )

        # Stop heater/controller on confirmed cancel.
        controller = getattr(self, "experiment_controller", None)
        if controller is not None:
            try:
                controller.stop()
            except Exception:
                pass

        # Return to Welcome screen.
        self.show("welcome")

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

    # ---------------- Flow actions ----------------
    def go_from_language(self):
        self.show("welcome")

    def go_from_welcome(self):
        self.show("setup_pdms")
        
    def confirm_pdms_ready(self):
        try:
            self.experiment_controller.start()
        except Exception:
            pass
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

    # ---------------- Simulation loops ----------------
    def _start_sim_for_screen(self, key: str):
        # cancel any prior sim tick loop
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
            # BaselineMeasurementScreen uses start_sim()
            if hasattr(self.frames["baseline"], "start_sim"):
                self.frames["baseline"].start_sim()

        elif key == "data_collection":
            # DataCollectionScreen uses start_sim()
            if hasattr(self.frames["data_collection"], "start_sim"):
                self.frames["data_collection"].start_sim()
            elif hasattr(self.frames["data_collection"], "simulate_progress"):
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

        # Stop ticking once ready (prevents background spam / lag)
        if self._sim["temp_ready"] and self._sim["stable_ready"]:
            self._sim_job = None
            return

        self._sim_job = self.after(300, self._tick_preheat_sim)



