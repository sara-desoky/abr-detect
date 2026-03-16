import tkinter as tk

from ui.config import COLORS, FONTS
from ui.rtl import rtl


class BaselineMeasurementScreen(tk.Frame):
    """
    Baseline is collected from controller readings on this screen.
    Rule used by backend: take 3 points, baseline = last point.
    """

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._sim_job = None

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
        if hasattr(self.app, "confirm_baseline_next"):
            self.app.confirm_baseline_next()
        else:
            self.app.show("load_antibiotic")

    def on_show(self):
        self.start_sim()

    # compatibility with old AppUI calls
    def start_sim(self):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("قياس خط الأساس"))
            self.subtitle_lbl.config(
                text=rtl("يتم جمع بيانات خط الأساس..."),
                fg=COLORS.get("accent_blue", COLORS["text"]),
            )
            self.next_btn.config(text=rtl("التالي"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Baseline Measurement")
            self.subtitle_lbl.config(
                text="Baseline data collection in progress...",
                fg=COLORS.get("accent_blue", COLORS["text"]),
            )
            self.next_btn.config(text="NEXT", font=FONTS["button"])

        self.next_btn.config(
            state="disabled",
            bg=COLORS.get("btn_disabled_bg", "#E6E6E6"),
            fg=COLORS.get("btn_disabled_text", "#777777"),
        )
        self._tick()

    def _tick(self):
        points = 0
        need = 3
        done = False
        baseline_hz = None
        try:
            p = self.app.experiment_controller.baseline_progress()
            points = int(p.get("points", 0))
            need = int(p.get("required_points", 3))
            done = bool(p.get("done", False))
            baseline_hz = p.get("baseline_hz")
        except Exception:
            pass

        baseline_txt = "N/A"
        if isinstance(baseline_hz, (int, float)):
            baseline_txt = f"{baseline_hz / 1e6:.6f} MHz"

        if self.app.lang == "ar":
            self.body_lbl.config(
                text=rtl(
                    "يرجى إبقاء الجهاز مغلقا دون اهتزاز.\n\n"
                    f"عينات خط الأساس: {points}/{need}\n"
                    f"آخر قيمة مقاسة: {baseline_txt}"
                ),
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
        else:
            self.body_lbl.config(
                text=(
                    "Please keep the device closed and undisturbed.\n\n"
                    f"Baseline samples: {points}/{need}\n"
                    f"Latest measured value: {baseline_txt}"
                ),
                font=FONTS["body"],
            )

        if done:
            green = COLORS.get("accent_green", COLORS.get("success", COLORS["text"]))
            if self.app.lang == "ar":
                self.subtitle_lbl.config(
                    text=rtl("تم إكمال قياس خط الأساس بنجاح"),
                    fg=green,
                )
            else:
                self.subtitle_lbl.config(
                    text="Baseline measurement successful!",
                    fg=green,
                )
            self.next_btn.config(
                state="normal",
                bg=COLORS["btn_bg"],
                fg=COLORS["btn_text"],
            )
            self._sim_job = None
            return

        self._sim_job = self.after(250, self._tick)
