# ui/screens/preheat.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class PreheatScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 10))

        self.status_lbl = tk.Label(self, text="", font=FONTS["subtitle"], bg=COLORS["bg"], fg=COLORS["danger"])
        self.status_lbl.grid(row=2, column=0, pady=(0, 18))

        self.body_lbl = tk.Label(
            self, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"],
            justify="center"
        )
        self.body_lbl.grid(row=3, column=0, padx=40, pady=(0, 18))

        self.temp_lbl = tk.Label(self, text="", font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.temp_lbl.grid(row=4, column=0, pady=(0, 8))

        self.stable_lbl = tk.Label(self, text="", font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.stable_lbl.grid(row=5, column=0, pady=(0, 22))

        self.next_btn = tk.Button(
            self,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=16,
            height=2,
            state="disabled",
            command=self.app.confirm_preheat_next,
        )
        self.next_btn.grid(row=6, column=0, pady=10)

        self.on_show()

    def on_show(self):
        wrap = int(max(600, self.app.winfo_width() * 0.85)) if self.app.winfo_width() > 1 else 700

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("تسخين الجهاز"))
            self.body_lbl.config(
                text=rtl("يرجى إبقاء الجهاز مغلقًا دون إزعاج أثناء التسخين."),
                wraplength=wrap,
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
            self.next_btn.config(text=rtl("التالي"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Preheating Device")
            self.body_lbl.config(
                text="Please keep the device closed and undisturbed while heating takes place.",
                wraplength=wrap,
                font=FONTS["body"],
            )
            self.next_btn.config(text="NEXT", font=FONTS["button"])

        # default state text
        self.status_lbl.config(text="Heating in progress...", fg=COLORS["danger"])
        self.temp_lbl.config(text="Current: -- °C    Target: 25.0 °C")
        self.stable_lbl.config(text="Stable samples: 0/10")

    def set_state(
        self,
        current_c: float | None,
        target_c: float,
        stable_got: int,
        stable_need: int,
        temp_ready: bool,
        stable_ready: bool,
    ):
        if current_c is None:
            self.temp_lbl.config(text=f"Current: -- °C    Target: {target_c:.1f} °C")
        else:
            self.temp_lbl.config(text=f"Current: {current_c:.1f} °C    Target: {target_c:.1f} °C")

        self.stable_lbl.config(text=f"Stable samples: {stable_got}/{stable_need}")

        # ✅ Status transition (your mockup)
        if temp_ready:
            self.status_lbl.config(text="Optimal temperature reached", fg=COLORS["success"])
        else:
            self.status_lbl.config(text="Heating in progress...", fg=COLORS["danger"])

        # ✅ NEXT enabled only when BOTH ready
        if temp_ready and stable_ready:
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
        else:
            self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])
