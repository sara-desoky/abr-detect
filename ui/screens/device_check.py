# ui/screens/device_check.py
import tkinter as tk
from ui.config import COLORS, FONTS


class DeviceCheckScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.grid(row=0, column=0, sticky="nsew")

        self.title = tk.Label(
            self.content,
            text="Device Check",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.title.pack(pady=(80, 20))

        self.body = tk.Label(
            self.content,
            text="Confirm device is ready.",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=800,
        )
        self.body.pack(pady=(0, 40))

        self.button = tk.Button(
            self.content,
            text="START",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self._on_press,
        )
        self.button.pack()

        self.current_phase = None

    def configure_phase(self, phase):
        """
        Called by app_ui to change behavior
        """
        self.current_phase = phase

        if phase == "baseline":
            self.body.config(
                text="Confirm the device lid is closed and NanoVNA is ready.\n\nPress START to begin baseline measurement."
            )
        else:
            self.body.config(
                text="Confirm device is ready for antibiotic data collection.\n\nPress START to begin data collection."
            )

    def _on_press(self):
        if self.current_phase == "baseline":
            self.app.simulate_next("device_check_1")
        else:
            self.app.simulate_next("device_check_2")
