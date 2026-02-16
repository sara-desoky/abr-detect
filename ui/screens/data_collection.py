# ui/screens/data_collection.py
import tkinter as tk
from ui.config import COLORS, FONTS


class DataCollectionScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._sim_job = None
        self._pct = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        tk.Label(content, text="Data Collection", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 10)
        )

        self.subtitle_lbl = tk.Label(
            content, text="Data collection in progress...", font=FONTS["button"], fg=COLORS["accent_blue"], bg=COLORS["bg"]
        )
        self.subtitle_lbl.grid(row=2, column=0, pady=(0, 18))

        tk.Label(
            content,
            text="Please keep the device closed and undisturbed. This\nmeasurement will take approximately 12 minutes.",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        ).grid(row=3, column=0, pady=(0, 22), padx=40)

        self.bar_canvas = tk.Canvas(content, width=520, height=18, bg=COLORS["bg"], highlightthickness=0)
        self.bar_canvas.grid(row=4, column=0, pady=(0, 8))
        self.bar_canvas.create_rectangle(0, 0, 520, 18, outline="#333333", width=1)
        self.bar_fg = self.bar_canvas.create_rectangle(0, 0, 0, 18, outline="", fill=COLORS["accent_blue"])

        self.timer_lbl = tk.Label(content, text="12:00", font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["text"])
        self.timer_lbl.grid(row=5, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            content,
            text="NEXT",
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=18,
            height=2,
            state="disabled",
            command=lambda: self.app.simulate_next("data_collection"),
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def start_sim(self):
        self._pct = 0
        self.subtitle_lbl.config(text="Data collection in progress...", fg=COLORS["accent_blue"])
        self.timer_lbl.config(text="12:00")
        self.bar_canvas.coords(self.bar_fg, 0, 0, 0, 18)
        self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])

        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._tick()

    def _tick(self):
        self._pct += 10
        if self._pct >= 100:
            self.subtitle_lbl.config(text="Data collection successful!", fg=COLORS["accent_green"])
            self.bar_canvas.coords(self.bar_fg, 0, 0, 520, 18)
            self.timer_lbl.config(text="00:00")
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
            return

        w = int(520 * (self._pct / 100.0))
        self.bar_canvas.coords(self.bar_fg, 0, 0, w, 18)

        mins = max(0, 12 - (self._pct // 10))
        self.timer_lbl.config(text=f"{mins:02d}:00")

        self._sim_job = self.after(350, self._tick)
