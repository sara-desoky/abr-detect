# ui/screens/preheat.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class PreheatScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(6, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Preheating Device" if self.app.lang != "ar" else rtl("تسخين الجهاز")
        subtitle = (
            "Please wait while the device reaches 25°C."
            if self.app.lang != "ar"
            else rtl("يرجى الانتظار حتى يصل الجهاز إلى ٢٥ درجة مئوية.")
        )

        tk.Label(
            content,
            text=title,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        ).grid(row=1, column=0, pady=(0, 14))

        tk.Label(
            content,
            text=subtitle,
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS.get("muted", "#666666"),
            justify="center",
        ).grid(row=2, column=0, pady=(0, 18))

        self.temp_lbl = tk.Label(
            content,
            text="Current: -- °C   Target: 25.0 °C",
            font=FONTS.get("body_small", ("Arial", 14)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        self.temp_lbl.grid(row=3, column=0, pady=(0, 18))

        # Optional stop button (nice for testing)
        self.stop_btn = tk.Button(
            content,
            text="STOP" if self.app.lang != "ar" else rtl("إيقاف"),
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self.app.stop_all,
        )
        self.stop_btn.grid(row=4, column=0, pady=10)

    def set_temp(self, current_c, target_c: float):
        if current_c is None:
            self.temp_lbl.config(text=f"Current: -- °C   Target: {target_c:.1f} °C")
        else:
            self.temp_lbl.config(text=f"Current: {current_c:.1f} °C   Target: {target_c:.1f} °C")
