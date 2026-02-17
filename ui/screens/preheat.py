# ui/screens/preheat.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class PreheatScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(9, weight=1)

        self.title_lbl = tk.Label(self.content, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 10))

        self.status_lbl = tk.Label(self.content, font=FONTS["subtitle"], bg=COLORS["bg"], fg=COLORS["danger"])
        self.status_lbl.grid(row=2, column=0, pady=(0, 14))

        self.body_lbl = tk.Label(self.content, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.body_lbl.grid(row=3, column=0, pady=(0, 14))

        self.temp_lbl = tk.Label(self.content, font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.temp_lbl.grid(row=4, column=0, pady=(0, 6))

        self.stable_lbl = tk.Label(self.content, font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["muted"])
        self.stable_lbl.grid(row=5, column=0, pady=(0, 18))

        self.next_btn = tk.Button(
            self.content,
            font=FONTS["button"],
            bg=COLORS["btn_disabled_bg"],
            fg=COLORS["btn_disabled_text"],
            width=20,
            height=2,
            state="disabled",
            command=self.app.confirm_preheat_next,
        )
        self.next_btn.grid(row=6, column=0, pady=(0, 10))

        self.on_show()

    def _wrap(self) -> int:
        w = self.winfo_toplevel().winfo_width()
        if w <= 1:
            w = self.winfo_toplevel().winfo_screenwidth()
        return int(w * 0.80)

    def on_show(self):
        self.body_lbl.config(wraplength=self._wrap())
        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("تسخين الجهاز"))
            self.next_btn.config(text=rtl("التالي"))
        else:
            self.title_lbl.config(text="Preheating Device")
            self.next_btn.config(text="NEXT")

        self.set_state(None, 25.0, 0, 10, False, False)

    def set_state(self, current_c, target_c, stable_got, stable_need, temp_ready, stable_ready):
        self.body_lbl.config(wraplength=self._wrap())

        if temp_ready:
            self.status_lbl.config(
                text=("Optimal temperature reached" if self.app.lang != "ar" else rtl("تم الوصول لدرجة الحرارة المثلى")),
                fg=COLORS["success"],
            )
            self.body_lbl.config(
                text=(
                    "Please ensure that the blue light inside the device is on and press Next."
                    if self.app.lang != "ar"
                    else rtl("يرجى التأكد من أن الضوء الأزرق داخل الجهاز قيد التشغيل ثم اضغط التالي.")
                )
            )
        else:
            self.status_lbl.config(
                text=("Heating in progress..." if self.app.lang != "ar" else rtl("...جارٍ التسخين")),
                fg=COLORS["danger"],
            )
            self.body_lbl.config(
                text=(
                    "Please keep the device closed and undisturbed while heating takes place."
                    if self.app.lang != "ar"
                    else rtl("يرجى إبقاء الجهاز مغلقًا ودون إزعاج أثناء التسخين.")
                )
            )

        if current_c is None:
            self.temp_lbl.config(text=f"Current: -- °C   Target: {target_c:.1f} °C")
        else:
            self.temp_lbl.config(text=f"Current: {current_c:.1f} °C   Target: {target_c:.1f} °C")

        self.stable_lbl.config(text=f"Stable samples: {stable_got}/{stable_need}")

        ready = bool(temp_ready and stable_ready)
        if ready:
            self.next_btn.config(state="normal", bg=COLORS["btn_bg"], fg=COLORS["btn_text"])
        else:
            self.next_btn.config(state="disabled", bg=COLORS["btn_disabled_bg"], fg=COLORS["btn_disabled_text"])
