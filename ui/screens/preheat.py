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
        self.temp_ready = False
        self.stable_ready = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Preheating Device" if app.lang != "ar" else rtl("تسخين الجهاز")
        subtitle = "Heating in progress..." if app.lang != "ar" else rtl("التسخين جارٍ...")

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 10)
        )
        tk.Label(content, text=subtitle, font=FONTS["button"], bg=COLORS["bg"], fg=COLORS["accent_red"]).grid(
            row=2, column=0, pady=(0, 18)
        )

        body = (
            "Please keep the device closed and undisturbed while heating takes place."
            if app.lang != "ar"
            else rtl("يرجى إبقاء الجهاز مغلقًا دون إزعاج أثناء التسخين.")
        )
        tk.Label(content, text=body, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"],
                 justify="center", wraplength=850).grid(row=3, column=0, pady=(0, 18))

        self.temp_lbl = tk.Label(content, text="Current: -- °C   Target: 25.0 °C",
                                 font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.temp_lbl.grid(row=4, column=0, pady=(0, 8))

        self.stable_lbl = tk.Label(content, text="Stable samples: 0/10",
                                   font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.stable_lbl.grid(row=5, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            content,
            text="NEXT" if app.lang != "ar" else rtl("التالي"),
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=16,
            height=2,
            state="disabled",
            command=self.app.confirm_preheat_next,
        )
        self.next_btn.grid(row=6, column=0, pady=10)

    def set_temp(self, current_c, target_c: float, temp_ready: bool):
        self.temp_ready = bool(temp_ready)
        if current_c is None:
            self.temp_lbl.config(text=f"Current: -- °C   Target: {target_c:.1f} °C")
        else:
            self.temp_lbl.config(text=f"Current: {current_c:.1f} °C   Target: {target_c:.1f} °C")
        self._update_next()

    def set_stability(self, got: int, need: int, stable_ready: bool):
        self.stable_ready = bool(stable_ready)
        self.stable_lbl.config(text=f"Stable samples: {got}/{need}")
        self._update_next()

    def _update_next(self):
        can_next = self.temp_ready and self.stable_ready
        if can_next:
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
        else:
            self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])
