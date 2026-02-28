# ui/screens/data_collection.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class DataCollectionScreen(tk.Frame):
    """
    Simulation:
      - Runs fast (few seconds) and enables NEXT.
      - Works if AppUI calls on_show(), start_sim(), or simulate_progress().
      - Keeps NEXT visible (prevents clipping off-screen).
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self._sim_job = None
        self._pct = 0

        # Fast sim tuning
        self._tick_ms = 180
        self._pct_step = 8

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.grid(row=0, column=0, sticky="nsew", padx=40, pady=30)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)   # top spacer
        self.content.grid_rowconfigure(99, weight=1)  # bottom spacer

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
            fg=COLORS["accent_blue"],
            bg=COLORS["bg"],
        )
        self.subtitle_lbl.grid(row=2, column=0, pady=(0, 14))

        self.body_lbl = tk.Label(
            self.content,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        self.body_lbl.grid(row=3, column=0, pady=(0, 18))

        self.bar_canvas = tk.Canvas(
            self.content, width=520, height=18, bg=COLORS["bg"], highlightthickness=0
        )
        self.bar_canvas.grid(row=4, column=0, pady=(0, 8))
        self.bar_canvas.create_rectangle(0, 0, 520, 18, outline="#333333", width=1)
        self.bar_fg = self.bar_canvas.create_rectangle(
            0, 0, 0, 18, outline="", fill=COLORS["accent_blue"]
        )

        self.timer_lbl = tk.Label(
            self.content,
            text="12:00",
            font=FONTS["small"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.timer_lbl.grid(row=5, column=0, pady=(0, 14))

        self.next_btn = tk.Button(
            self.content,
            text="NEXT",
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=18,
            height=2,
            state="disabled",
            command=self._go_next,
        )
        self.next_btn.grid(row=6, column=0, pady=(8, 0))

    def _go_next(self):
        if hasattr(self.app, "confirm_data_collection_next"):
            self.app.confirm_data_collection_next()

    # compatibility
    def simulate_progress(self):
        self.start_sim()

    def on_show(self):
        self._apply_wrap()
        self._apply_language()
        self.start_sim()

    def _apply_wrap(self):
        w = self.app.winfo_width()
        wrap = int(max(520, w * 0.85)) if w and w > 1 else 820
        self.body_lbl.config(wraplength=wrap)

    def start_sim(self):
        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._pct = 0
        if self.app.lang == "ar":
            self.subtitle_lbl.config(
                text=rtl("جمع البيانات جارٍ..."),
                fg=COLORS["accent_blue"],
                font=FONTS.get("arabic_button", FONTS["button"]),
            )
        else:
            self.subtitle_lbl.config(
                text="Data collection in progress...",
                fg=COLORS["accent_blue"],
                font=FONTS["button"],
            )
        self.timer_lbl.config(text="12:00")
        self.bar_canvas.coords(self.bar_fg, 0, 0, 0, 18)
        self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])

        self._tick()

    def _tick(self):
        self._pct += self._pct_step

        if self._pct >= 100:
            self._pct = 100
            green = COLORS.get("accent_green", COLORS.get("success", COLORS["accent"]))
            if self.app.lang == "ar":
                self.subtitle_lbl.config(
                    text=rtl("اكتمل جمع البيانات بنجاح!"),
                    fg=green,
                    font=FONTS.get("arabic_button", FONTS["button"]),
                )
            else:
                self.subtitle_lbl.config(text="Data collection successful!", fg=green, font=FONTS["button"])
            self.bar_canvas.coords(self.bar_fg, 0, 0, 520, 18)
            self.timer_lbl.config(text="00:00")
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
            self._sim_job = None
            return

        w = int(520 * (self._pct / 100.0))
        self.bar_canvas.coords(self.bar_fg, 0, 0, w, 18)

        total_minutes = 12
        minutes_left = max(0, total_minutes - int((self._pct / 100.0) * total_minutes))
        self.timer_lbl.config(text=f"{minutes_left:02d}:00")

        self._sim_job = self.after(self._tick_ms, self._tick)

    def _apply_language(self):
        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("جمع البيانات"), font=FONTS["title"])
            self.body_lbl.config(
                text=rtl(
                    "يرجى إبقاء الجهاز مغلقًا دون إزعاج. سيستغرق هذا\n"
                    "القياس حوالي 12 دقيقة."
                ),
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
            self.next_btn.config(text=rtl("التالي"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Data Collection", font=FONTS["title"])
            self.body_lbl.config(
                text=(
                    "Please keep the device closed and undisturbed. This\n"
                    "measurement will take approximately 12 minutes."
                ),
                font=FONTS["body"],
            )
            self.next_btn.config(text="NEXT", font=FONTS["button"])
