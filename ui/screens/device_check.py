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
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 14))

        self.block = tk.Frame(self, bg=COLORS["bg"])
        self.block.grid(row=2, column=0, sticky="n", padx=60)

        self.confirm_lbl = tk.Label(self.block, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], anchor="w", justify="left")
        self.confirm_lbl.grid(row=0, column=0, sticky="w")

        self.bullets_lbl = tk.Label(
            self.block,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="left",     # ✅ left align
            anchor="w"          # ✅ left anchor
        )
        self.bullets_lbl.grid(row=1, column=0, sticky="w", pady=(6, 10))

        self.footer_lbl = tk.Label(self, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.footer_lbl.grid(row=3, column=0, padx=40, pady=(10, 18))

        self.start_btn = tk.Button(
            self,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self._on_start,
        )
        self.start_btn.grid(row=4, column=0, pady=(0, 10))

        self.on_show()

    def set_phase(self, phase: str):
        self.phase = phase
        self.on_show()

    def _on_start(self):
        if self.phase == "baseline":
            self.app.confirm_device_check_baseline_start()
        else:
            self.app.confirm_device_check_collection_start()

    def on_show(self):
        # wrap bullets based on actual width
        wrap = int(max(520, self.app.winfo_width() * 0.75)) if self.app.winfo_width() > 1 else 620
        self.bullets_lbl.config(wraplength=wrap)

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("فحص الجهاز"))
            self.confirm_lbl.config(text=rtl("تأكد من التالي:"), font=FONTS.get("arabic_body", FONTS["body"]))
            bullets = [
                rtl("• غطاء الجهاز مغلق تمامًا"),
                rtl("• جهاز NanoVNA يعمل"),
                rtl("• شاشة NanoVNA تطابق شاشة المرجع في دليل التعليمات"),
            ]
            self.bullets_lbl.config(text="\n".join(bullets), font=FONTS.get("arabic_body", FONTS["body"]))
            if self.phase == "baseline":
                self.footer_lbl.config(text=rtl("بعد التأكد، اضغط ابدأ لبدء جمع بيانات خط الأساس."),
                                       font=FONTS.get("arabic_body", FONTS["body"]))
            else:
                self.footer_lbl.config(text=rtl("بعد التأكد، اضغط ابدأ لبدء جمع البيانات."),
                                       font=FONTS.get("arabic_body", FONTS["body"]))
            self.start_btn.config(text=rtl("ابدأ"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Device Check")
            self.confirm_lbl.config(text="Confirm that:", font=FONTS["body"])
            bullets = [
                "• The device lid is fully closed",
                "• The NanoVNA is powered on",
                "• The NanoVNA display matches the reference\n  screen shown in the Instruction Manual",
            ]
            self.bullets_lbl.config(text="\n".join(bullets), font=FONTS["body"])
            if self.phase == "baseline":
                self.footer_lbl.config(text="Once confirmed, press START to begin baseline data collection", font=FONTS["body"])
            else:
                self.footer_lbl.config(text="Once confirmed, press START to begin data collection.", font=FONTS["body"])
            self.start_btn.config(text="START", font=FONTS["button"])
