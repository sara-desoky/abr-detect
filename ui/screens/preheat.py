import tkinter as tk
from ui.config import COLORS, FONTS


class PreheatScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.temp_ready = False
        self.stable_ready = False

        self.title_lbl = tk.Label(
            self,
            text="Preheating Device",
            font=("Times New Roman", 40, "bold"),
            bg=COLORS["bg"],
        )
        self.title_lbl.pack(pady=(80, 20))

        self.status_lbl = tk.Label(
            self,
            text="Heating in progress...",
            font=("Arial", 26, "bold"),
            fg="#C44536",
            bg=COLORS["bg"],
        )
        self.status_lbl.pack(pady=10)

        self.desc_lbl = tk.Label(
            self,
            text="Please keep the device closed and undisturbed while heating takes place.",
            font=("Arial", 20),
            wraplength=900,
            justify="center",
            bg=COLORS["bg"],
        )
        self.desc_lbl.pack(pady=20)

        self.progress_lbl = tk.Label(
            self,
            text="Stable samples: 0/10",
            font=("Arial", 16),
            fg="#666666",
            bg=COLORS["bg"],
        )
        self.progress_lbl.pack(pady=10)

        self.next_btn = tk.Button(
            self,
            text="NEXT",
            font=("Times New Roman", 24, "bold"),
            width=14,
            height=2,
            state="disabled",
            command=lambda: app.simulate_next("preheat"),
        )
        self.next_btn.pack(pady=40)

        # SIMULATION shortcut
        self.after(1500, self.simulate_ready)

    def simulate_ready(self):
        self.temp_ready = True
        self.stable_ready = True
        self.update_state()

    def update_state(self):
        if self.temp_ready and self.stable_ready:
            self.status_lbl.config(
                text="Optimal temperature reached",
                fg="#2D6A4F",
            )
            self.next_btn.config(state="normal")
