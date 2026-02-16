import tkinter as tk
from ui.config import COLORS


class ResultScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])

        tk.Label(
            self,
            text="Result: ESBL Negative",
            font=("Times New Roman", 40, "bold"),
            bg=COLORS["bg"],
        ).pack(pady=(80, 30))

        tk.Label(
            self,
            text="Baseline resonance: ___ MHz\nFrequency shift: ___ MHz",
            font=("Arial", 20),
            bg=COLORS["bg"],
        ).pack(pady=10)

        tk.Label(
            self,
            text="The observed frequency shift does not exceed the detection threshold and is not consistent with ESBL activity.",
            font=("Arial", 18),
            wraplength=900,
            justify="center",
            bg=COLORS["bg"],
        ).pack(pady=20)

        tk.Button(
            self,
            text="FINISH",
            font=("Times New Roman", 24, "bold"),
            width=14,
            height=2,
            command=app.destroy,
        ).pack(pady=40)
