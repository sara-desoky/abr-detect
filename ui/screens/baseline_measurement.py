# ui/screens/baseline_measurement.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


class BaselineMeasurementScreen(tk.Frame):
    """
    Figma has two states:
      1) "Baseline data collection in progress..."
      2) "Baseline measurement successful!" + NEXT enabled

    Simulation: auto-completes quickly when screen is shown.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self._sim_job = None
        self._sim_step = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.grid(row=0, column=0, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(10, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(
            self.content,
            text="",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.title_lbl.grid(row=1, column=0, pady=(0, 10))

        self.subtitle_lbl = tk.Label(
            self.content,
            text="",
            font=FONTS["button"],
            bg=COLORS["bg"],
            fg=COLORS.get("accent_blue", COLORS["text"]),
        )
        self.subtitle_lbl.grid(row=2, column=0, pady=(0, 18))

        self.body_lbl = tk.Label(
            self.content,
            text="",
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        )
        self.body_lbl.grid(row=3, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            self.content,
            text="NEXT",
            font=FONTS["button"],
            bg=COLORS.get("btn_disabled_bg", "#E6E6E6"),
            fg=COLORS.get("btn_disabled_text", "#777777"),
            width=18,
            height=2,
            state="disabled",
            command=self._on_next,
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def _on_next(self):
        # Use your real AppUI flow method
        if hasattr(self.app, "confirm_baseline_next"):
            self.app.confirm_baseline_next()
        else:
            # fallback
            self.app.show("load_antibiotic")

    def on_show(self):
        # Refresh language + restart the simulation each time we enter this screen
        self.start_sim()

    def start_sim(self):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._sim_step = 0

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("قياس خط الأساس"))
            self.subtitle_lbl.config(text=rtl("جارٍ جمع بيانات خط الأساس..."),
                                     fg=COLORS.get("accent_blue", COLORS["text"]))
            self.body_lbl.config(text=rtl(
                "يرجى إبقاء الجهاز مغلقًا دون إزعاج.\n"
                "سيستغرق هذا القياس الأولي حوالي 7 دقائق.\n\n"
                "عينات مستقرة: ٠/١٠"
            ))
            self.next_btn.config(text=rtl("التالي"))
        else:
            self.title_lbl.config(text="Baseline Measurement")
            self.subtitle_lbl.config(text="Baseline data collection in progress...",
                                     fg=COLORS.get("accent_blue", COLORS["text"]))
            self.body_lbl.config(
                text="Please keep the device closed and undisturbed. This\n"
                     "initial measurement will take approximately 7 minutes.\n\n"
                     "Stable samples: 0/10"
            )
            self.next_btn.config(text="NEXT")

        self.next_btn.config(
            state="disabled",
            bg=COLORS.get("btn_disabled_bg", "#E6E6E6"),
            fg=COLORS.get("btn_disabled_text", "#777777"),
        )

        self._tick_sim()

    def _tick_sim(self):
        self._sim_step += 2
        if self._sim_step >= 10:
            self._set_success()
            return

        if self.app.lang == "ar":
            self.body_lbl.config(text=rtl(
                "يرجى إبقاء الجهاز مغلقًا دون إزعاج.\n"
                "سيستغرق هذا القياس الأولي حوالي 7 دقائق.\n\n"
                f"عينات مستقرة: {self._sim_step}/١٠"
            ))
        else:
            self.body_lbl.config(
                text="Please keep the device closed and undisturbed. This\n"
                     "initial measurement will take approximately 7 minutes.\n\n"
                     f"Stable samples: {self._sim_step}/10"
            )

        self._sim_job = self.after(300, self._tick_sim)

    def _set_success(self):
        if self.app.lang == "ar":
            self.subtitle_lbl.config(text=rtl("اكتمل قياس خط الأساس بنجاح!"),
                                     fg=COLORS.get("accent_green", COLORS["text"]))
            self.body_lbl.config(text=rtl(
                "يرجى الضغط على التالي وتجهيز محلول المضاد الحيوي\n"
                "مع المحقنة 100µL."
            ))
        else:
            self.subtitle_lbl.config(text="Baseline measurement successful!",
                                     fg=COLORS.get("accent_green", COLORS["text"]))
            self.body_lbl.config(
                text="Please press Next and have the antibiotic solution ready\n"
                     "along with the provided 100µL syringe."
            )

        self.next_btn.config(
            state="normal",
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
        )
