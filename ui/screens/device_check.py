# ui/screens/device_check.py
import tkinter as tk

class DeviceCheckScreen(tk.Frame):
    def __init__(self, parent, on_start=None):
        super().__init__(parent, bg="white")
        self.on_start = on_start

        tk.Label(self, text="Device Check", font=("Times New Roman", 30, "bold"),
                 bg="white").pack(pady=(30, 10))

        body = (
            "Confirm that:\n"
            "• The device lid is fully closed\n"
            "• The VNA is powered on\n"
            "• Cables are connected properly\n\n"
            "Press START to begin data collection."
        )
        tk.Label(self, text=body, font=("Arial", 14), bg="white", justify="left").pack(pady=(0, 18))

        tk.Button(self, text="START", font=("Times New Roman", 18, "bold"),
                  width=14, command=self._start).pack()

    def _start(self):
        if self.on_start:
            self.on_start()
