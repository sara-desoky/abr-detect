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

    Option A simulation: auto-completes quickly.
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self._sim_job = None
        self._sim_step = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Baseline Measurement" if app.lang != "ar" else rtl("قياس خط الأساس")

        self.subtitle_lbl = tk.Label(
            content,
            text="Baseline data collection in progress..." if app.lang != "ar" else rtl("جارٍ جمع بيانات خط الأساس..."),
            font=FONTS["button"],
            bg=COLORS["bg"],
            fg=COLORS["accent_blue"],
        )

        self.body_lbl = tk.Label(
            content,
            text="",
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        )

        tk.Label(
            content,
            text=title,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).grid(row=1, column=0, pady=(0, 10))

        self.subtitle_lbl.grid(row=2, column=0, pady=(0, 18))
        self.body_lbl.grid(row=3, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            content,
            text="NEXT" if app.lang != "ar" else rtl("التالي"),
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=18,
            height=2,
            state="disabled",
            command=lambda: self.app.simulate_next("baseline"),
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def start_sim(self):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._sim_step = 0
        self.subtitle_lbl.config(
            text="Baseline data collection in progress..." if self.app.lang != "ar" else rtl("جارٍ جمع بيانات خط الأساس..."),
            fg=COLORS["accent_blue"],
        )
        self.body_lbl.config(
            text=(
                "Please keep the device closed and undisturbed. This\n"
                "initial measurement will take approximately 7 minutes.\n\n"
                "Stable samples: 0/10"
                if self.app.lang != "ar"
                else rtl("يرجى إبقاء الجهاز مغلقًا دون إزعاج.\n\nعينات مستقرة: ٠/١٠")
            )
        )
        self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])

        self._tick_sim()

    def _tick_sim(self):
        self._sim_step += 2
        if self._sim_step >= 10:
            self._set_success()
            return

        self.body_lbl.config(
            text=(
                "Please keep the device closed and undisturbed. This\n"
                "initial measurement will take approximately 7 minutes.\n\n"
                f"Stable samples: {self._sim_step}/10"
            )
        )
        self._sim_job = self.after(300, self._tick_sim)

    def _set_success(self):
        self.subtitle_lbl.config(text="Baseline measurement successful!", fg=COLORS["accent_green"])
        self.body_lbl.config(
            text="Please press Next and have the antibiotic solution ready\nalong with the provided 100µL syringe."
        )
        self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
