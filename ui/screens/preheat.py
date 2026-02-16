# ui/screens/preheat.py
import tkinter as tk
from ui.config import COLORS, FONTS


class PreheatScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.temp_ready = False
        self.stable_got = 0
        self.stable_need = 10

        self._sim_job = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        tk.Label(
            content,
            text="Preheating Device",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).grid(row=1, column=0, pady=(0, 10))

        self.status_lbl = tk.Label(
            content,
            text="Heating in progress...",
            font=FONTS["button"],
            fg=COLORS["accent_red"],
            bg=COLORS["bg"],
        )
        self.status_lbl.grid(row=2, column=0, pady=(0, 18))

        self.desc_lbl = tk.Label(
            content,
            text="Please keep the device closed and undisturbed while heating takes place.",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            wraplength=820,
            justify="center",
        )
        self.desc_lbl.grid(row=3, column=0, pady=(0, 18), padx=40)

        self.temp_lbl = tk.Label(
            content,
            text="Current: -- °C   Target: 25.0 °C",
            font=FONTS["small"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        )
        self.temp_lbl.grid(row=4, column=0, pady=(0, 6))

        self.progress_lbl = tk.Label(
            content,
            text="Stable samples: 0/10",
            font=FONTS["small"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        )
        self.progress_lbl.grid(row=5, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            content,
            text="NEXT",
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=18,
            height=2,
            state="disabled",
            command=self.app.confirm_preheat_next,
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def start_sim(self):
        self.temp_ready = False
        self.stable_got = 0

        self.status_lbl.config(text="Heating in progress...", fg=COLORS["accent_red"])
        self.desc_lbl.config(text="Please keep the device closed and undisturbed while heating takes place.")
        self.temp_lbl.config(text="Current: 22.0 °C   Target: 25.0 °C")
        self.progress_lbl.config(text=f"Stable samples: {self.stable_got}/{self.stable_need}")
        self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])

        if self._sim_job is not None:
            try:
                self.after_cancel(self._sim_job)
            except Exception:
                pass
            self._sim_job = None

        self._tick_sim()

    def _tick_sim(self):
        if not self.temp_ready:
            self.temp_ready = True
            self.temp_lbl.config(text="Current: 25.0 °C   Target: 25.0 °C")

        if self.stable_got < self.stable_need:
            self.stable_got += 2
            if self.stable_got > self.stable_need:
                self.stable_got = self.stable_need
            self.progress_lbl.config(text=f"Stable samples: {self.stable_got}/{self.stable_need}")

        if self.temp_ready and self.stable_got >= self.stable_need:
            self.status_lbl.config(text="Optimal temperature reached", fg=COLORS["accent_green"])
            self.desc_lbl.config(text="Please ensure that the blue light inside the device is on\nand press Next.")
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
            return

        self._sim_job = self.after(300, self._tick_sim)
