# ui/screens/wait_stability.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class WaitStabilityScreen(tk.Frame):
    def __init__(self, parent, app, title_key: str):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.title_key = title_key

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(7, weight=1)
        content.grid_columnconfigure(0, weight=1)

        if self.app.lang == "ar":
            if title_key == "preg":
                title = rtl("انتظار استقرار خط الأساس")
            else:
                title = rtl("انتظار استقرار الإشارة")
            body = rtl("يرجى إبقاء الجهاز ثابتًا ومغلقًا.")
        else:
            title = "Waiting for baseline to stabilize" if title_key == "preg" else "Waiting for signal to stabilize"
            body = "Please keep the device closed and undisturbed."

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 14)
        )
        tk.Label(content, text=body, font=FONTS.get("body", ("Arial", 16)), bg=COLORS["bg"],
                 fg=COLORS.get("muted", "#666666")).grid(row=2, column=0, pady=(0, 18))

        self.progress_lbl = tk.Label(
            content,
            text="Stable samples: 0/10 | Threshold: 0.06 MHz",
            font=FONTS.get("body_small", ("Arial", 14)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.progress_lbl.grid(row=3, column=0, pady=(0, 8))

        self.freq_lbl = tk.Label(
            content,
            text="Current resonance: -- MHz",
            font=FONTS.get("body_small", ("Arial", 14)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        self.freq_lbl.grid(row=4, column=0, pady=(0, 18))

    def set_progress(self, got: int, need: int, thresh_mhz: float):
        self.progress_lbl.config(text=f"Stable samples: {got}/{need} | Threshold: {thresh_mhz:.2f} MHz")

    def set_freq(self, freq_hz):
        if freq_hz is None:
            self.freq_lbl.config(text="Current resonance: -- MHz")
        else:
            self.freq_lbl.config(text=f"Current resonance: {freq_hz/1e6:.3f} MHz")
