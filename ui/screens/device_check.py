# ui/screens/device_check.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class DeviceCheckScreen(tk.Frame):
    def __init__(self, parent, app, phase: str = "baseline"):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.phase = phase  # "baseline" or "collection"

        # Slightly smaller fonts to avoid overflow
        self._body_font = FONTS.get("body", ("Arial", 16))
        self._body_font_sm = FONTS.get("body_sm", ("Arial", 14))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(
            self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]
        )
        self.title_lbl.grid(row=1, column=0, pady=(0, 10))

        # Left-aligned content block (NOT centered)
        self.block = tk.Frame(self, bg=COLORS["bg"])
        self.block.grid(row=2, column=0, sticky="nw", padx=60)
        self.block.grid_columnconfigure(0, weight=1)

        self.confirm_lbl = tk.Label(
            self.block,
            text="",
            font=self._body_font_sm,
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="w",
            justify="left",
        )
        self.confirm_lbl.grid(row=0, column=0, sticky="w")

        self.bullets_lbl = tk.Label(
            self.block,
            text="",
            font=self._body_font_sm,
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="left",
            anchor="w",
        )
        self.bullets_lbl.grid(row=1, column=0, sticky="w", pady=(6, 10))

        self.footer_lbl = tk.Label(
            self,
            text="",
            font=self._body_font_sm,
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        self.footer_lbl.grid(row=3, column=0, padx=50, pady=(8, 14))

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

    def _on_start(self):
        if self.phase == "baseline":
            if hasattr(self.app, "confirm_device_check_baseline_start"):
                self.app.confirm_device_check_baseline_start()
            elif hasattr(self.app, "simulate_next"):
                self.app.simulate_next("device_check_1")
        else:
            if hasattr(self.app, "confirm_device_check_collection_start"):
                self.app.confirm_device_check_collection_start()
            elif hasattr(self.app, "simulate_next"):
                self.app.simulate_next("device_check_2")

    def on_show(self):
        # Wrap based on actual window width so nothing runs off-screen
        w = self.app.winfo_width()
        wrap = int(max(520, w * 0.80)) if w and w > 1 else 700

        self.confirm_lbl.config(wraplength=wrap)
        self.bullets_lbl.config(wraplength=wrap)
        self.footer_lbl.config(wraplength=int(max(520, wrap)))

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("فحص الجهاز"))
            self.confirm_lbl.config(text=rtl("تأكد من التالي:"), font=self._body_font_sm)

            bullets = [
                rtl("• غطاء الجهاز مغلق تمامًا"),
                rtl("• جهاز NanoVNA يعمل"),
                rtl("• شاشة NanoVNA تطابق شاشة المرجع في دليل التعليمات"),
            ]
            self.bullets_lbl.config(text="\n".join(bullets), font=self._body_font_sm)

            if self.phase == "baseline":
                self.footer_lbl.config(
                    text=rtl("بعد التأكد، اضغط ابدأ لبدء جمع بيانات خط الأساس."),
                    font=self._body_font_sm,
                )
            else:
                self.footer_lbl.config(
                    text=rtl("بعد التأكد، اضغط ابدأ لبدء جمع البيانات."),
                    font=self._body_font_sm,
                )

            self.start_btn.config(text=rtl("ابدأ"), font=FONTS.get("arabic_button", FONTS["button"]))

        else:
            self.title_lbl.config(text="Device Check")
            self.confirm_lbl.config(text="Confirm that:", font=self._body_font_sm)

            bullets = [
                "• The device lid is fully closed",
                "• The NanoVNA is powered on",
                "• The NanoVNA display matches the reference screen\n  shown in the Instruction Manual",
            ]
            self.bullets_lbl.config(text="\n".join(bullets), font=self._body_font_sm)

            if self.phase == "baseline":
                self.footer_lbl.config(
                    text="Once confirmed, press START to begin baseline data collection",
                    font=self._body_font_sm,
                )
            else:
                self.footer_lbl.config(
                    text="Once confirmed, press START to begin data collection.",
                    font=self._body_font_sm,
                )

            self.start_btn.config(text="START", font=FONTS["button"])
