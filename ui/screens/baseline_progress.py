import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class BaselineProgressScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Baseline Measurement" if app.lang != "ar" else rtl("قياس خط الأساس")
        subtitle = "Baseline data collection in progress..." if app.lang != "ar" else rtl("جارٍ جمع بيانات خط الأساس...")

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 10)
        )
        tk.Label(content, text=subtitle, font=FONTS["button"], bg=COLORS["bg"], fg=COLORS["accent_blue"]).grid(
            row=2, column=0, pady=(0, 18)
        )

        body = (
            "Please keep the device closed and undisturbed.\n"
            "Baseline completes once the signal is stable."
            if app.lang != "ar"
            else rtl("يرجى إبقاء الجهاز مغلقًا دون إزعاج.\nيكتمل القياس عند استقرار الإشارة.")
        )
        tk.Label(content, text=body, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"],
                 justify="center", wraplength=850).grid(row=3, column=0, pady=(0, 18))

        self.stable_lbl = tk.Label(content, text="Stable samples: 0/10",
                                   font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.stable_lbl.grid(row=4, column=0, pady=(0, 8))

        self.freq_lbl = tk.Label(content, text="Current resonance: -- MHz",
                                 font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.freq_lbl.grid(row=5, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            content,
            text="NEXT" if app.lang != "ar" else rtl("التالي"),
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=16,
            height=2,
            state="disabled",
            command=lambda: self.app.show("load_antibiotic"),
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def set_freq(self, freq_hz):
        if freq_hz is None:
            self.freq_lbl.config(text="Current resonance: -- MHz")
        else:
            self.freq_lbl.config(text=f"Current resonance: {freq_hz/1e6:.3f} MHz")

    def set_stability(self, got: int, need: int, stable_ready: bool):
        self.stable_lbl.config(text=f"Stable samples: {got}/{need}")
        if stable_ready:
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
        else:
            self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])
