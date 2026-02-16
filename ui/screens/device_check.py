# ui/screens/device_check.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


class DeviceCheckScreen(tk.Frame):
    """
    One screen used twice:
      - phase="baseline": before baseline measurement (START -> baseline)
      - phase="collection": before data collection (START -> data_collection)
    """
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.phase = "baseline"  # default

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(
            content,
            text="Device Check" if app.lang != "ar" else rtl("فحص الجهاز"),
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.title_lbl.grid(row=1, column=0, pady=(0, 14))

        self.body_lbl = tk.Label(
            content,
            text="",
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        )
        self.body_lbl.grid(row=2, column=0, pady=(0, 18))

        self.start_btn = tk.Button(
            content,
            text="START" if app.lang != "ar" else rtl("ابدأ"),
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=self._on_start,
        )
        self.start_btn.grid(row=3, column=0, pady=10)

        self.configure_phase(self.phase)

    def configure_phase(self, phase: str):
        self.phase = phase

        if self.app.lang == "ar":
            if phase == "baseline":
                body = rtl("تأكد من إغلاق الغطاء وتشغيل جهاز NanoVNA.\nاضغط ابدأ لبدء قياس خط الأساس.")
            else:
                body = rtl("تأكد من إغلاق الغطاء.\nاضغط ابدأ لبدء جمع البيانات.")
        else:
            if phase == "baseline":
                body = (
                    "Confirm that:\n"
                    "• The device lid is fully closed\n"
                    "• The NanoVNA is powered on\n"
                    "• The NanoVNA display matches the reference\n"
                    "  screen shown in the Instruction Manual\n\n"
                    "Once confirmed, press START to begin baseline data\n"
                    "collection"
                )
            else:
                body = (
                    "Confirm that:\n"
                    "• The device lid is fully closed\n"
                    "• The NanoVNA display matches the reference\n"
                    "  screen shown in the Instruction Manual\n\n"
                    "Once confirmed, press START to begin data collection."
                )

        self.body_lbl.config(text=body)

    def _on_start(self):
        if self.phase == "baseline":
            self.app.simulate_next("device_check_1")
        else:
            self.app.simulate_next("device_check_2")
