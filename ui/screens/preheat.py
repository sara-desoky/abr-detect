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
        content.grid_rowconfigure(8, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Preheating Device" if self.app.lang != "ar" else rtl("تسخين الجهاز")
        subtitle = (
            "Please keep the device closed and undisturbed while heating takes place."
            if self.app.lang != "ar"
            else rtl("يرجى إبقاء الجهاز مغلقًا أثناء التسخين.")
        )

        tk.Label(
            content,
            text=title,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).grid(row=1, column=0, pady=(0, 10))

        tk.Label(
            content,
            text="Heating in progress...",
            font=("Arial", 20, "bold"),
            fg="#D84A3A",
            bg=COLORS["bg"],
        ).grid(row=2, column=0, pady=(0, 20))

        tk.Label(
            content,
            text=subtitle,
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            wraplength=850,
            justify="center",
        ).grid(row=3, column=0, pady=(0, 15))

        self.temp_lbl = tk.Label(
            content,
            text="Current: -- °C   Target: 25.0 °C",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        )
        self.temp_lbl.grid(row=4, column=0, pady=(0, 5))

        self.stable_lbl = tk.Label(
            content,
            text="Stable samples: 0/10",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
        )
        self.stable_lbl.grid(row=5, column=0, pady=(0, 20))

        self.next_btn = tk.Button(
            content,
            text="NEXT",
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=16,
            height=2,
            state="disabled",
            command=self.app.confirm_preheat_next,
        )
        self.next_btn.grid(row=6, column=0, pady=10)

        # ---- SIM MODE AUTO COMPLETE ----
        if getattr(self.app, "SIM_MODE", False):
            self.after(800, self._simulate_ready)

    def _simulate_ready(self):
        self.temp_lbl.config(text="Current: 25.0 °C   Target: 25.0 °C")
        self.stable_lbl.config(text="Stable samples: 10/10")

        self.next_btn.config(
            state="normal",
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
        )
