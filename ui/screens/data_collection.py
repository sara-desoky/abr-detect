import tkinter as tk
from ui.config import COLORS


class DataCollectionScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        tk.Label(
            self,
            text="Data Collection",
            font=("Times New Roman", 40, "bold"),
            bg=COLORS["bg"],
        ).pack(pady=(80, 20))

        tk.Label(
            self,
            text="Data collection in progress...",
            font=("Arial", 24, "bold"),
            fg="#2F3E73",
            bg=COLORS["bg"],
        ).pack(pady=10)

        tk.Label(
            self,
            text="Please keep the device closed and undisturbed.\nThis measurement will take approximately 12 minutes.",
            font=("Arial", 20),
            wraplength=900,
            justify="center",
            bg=COLORS["bg"],
        ).pack(pady=20)

        # Simulated progress bar
        self.progress = tk.Label(
            self,
            text="Simulating...",
            font=("Arial", 16),
            bg=COLORS["bg"],
        )
        self.progress.pack(pady=30)

        tk.Button(
            self,
            text="NEXT",
            font=("Times New Roman", 24, "bold"),
            width=14,
            height=2,
            command=lambda: app.simulate_next("data_collection"),
        ).pack(pady=40)
