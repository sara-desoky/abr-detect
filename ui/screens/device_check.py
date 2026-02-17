# ui/screens/device_check.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class DeviceCheckScreen(tk.Frame):
    def __init__(self, parent, app, phase: str = "baseline"):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.phase = phase  # "baseline" or "collection"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)

        self.title_lbl = tk.Label(content, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 8))

        self.confirm_lbl = tk.Label(content, font=FONTS["body_bold"], bg=COLORS["bg"], fg=COLORS["text"])
        self.confirm_lbl.grid(row=2, column=0, pady=(0, 6), sticky="w")

        self.bullets_lbl = tk.Label(
            content, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="left", anchor="w"
        )
        self.bullets_lbl.grid(row=3, column=0, pady=(0, 14), sticky="w")

        self.footer_lbl = tk.Label(
            content, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="left", anchor="w"
        )
        self.footer_lbl.grid(row=4, column=0, pady=(0, 18), sticky="w")

        self.start_btn = tk.Button(
            content,
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=20,
            height=2,
            command=self._on_start,
        )
        self.start_btn.grid(row=5, column=0, pady=(0, 10))

        self.on_show()

    def _wrap(self) -> int:
        w = self.winfo_toplevel().winfo_width()
        if w <= 1:
            w = self.winfo_toplevel().winfo_screenwidth()
        return int(w * 0.85)

    def on_show(self):
        wl = self._wrap()
        self.bullets_lbl.config(wraplength=wl)
        self.footer_lbl.config(wraplength=wl)

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("فحص الجهاز"))
            self.confirm_lbl.config(text=rtl("يرجى التأكد من:"))
            self.bullets_lbl.config(
                text="\n".join(
                    [
                        rtl("• أن غطاء الجهاز مغلق بالكامل"),
                        rtl("• أن جهاز NanoVNA قيد التشغيل"),
                        rtl("• أن شاشة NanoVNA تطابق الشاشة المرجعية في دليل التعليمات"),
                    ]
                )
            )
            self.start_btn.config(text=rtl("ابدأ"))
            self.footer_lbl.config(
                text=rtl("بعد التأكيد، اضغط ابدأ لبدء جمع بيانات خط الأساس.")
                if self.phase == "baseline"
                else rtl("بعد التأكيد، اضغط ابدأ لبدء جمع البيانات.")
            )
        else:
            self.title_lbl.config(text="Device Check")
            self.confirm_lbl.config(text="Confirm that:")
            self.bullets_lbl.config(
                text="\n".join(
                    [
                        "• The device lid is fully closed",
                        "• The NanoVNA is powered on",
                        "• The NanoVNA display matches the reference\n  screen shown in the Instruction Manual",
                    ]
                )
            )
            self.start_btn.config(text="START")
            self.footer_lbl.config(
                text="Once confirmed, press START to begin baseline data collection"
                if self.phase == "baseline"
                else "Once confirmed, press START to begin data collection"
            )

    def _on_start(self):
        if self.phase == "baseline":
            self.app.confirm_device_check_baseline_start()
        else:
            self.app.confirm_device_check_collection_start()
