# ui/screens/result_screen.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class ResultScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 16))

        self.metrics_lbl = tk.Label(self, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.metrics_lbl.grid(row=2, column=0, pady=(0, 18))

        self.body_lbl = tk.Label(self, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.body_lbl.grid(row=3, column=0, padx=50, pady=(0, 22))

        btn_row = tk.Frame(self, bg=COLORS["bg"])
        btn_row.grid(row=4, column=0, pady=10)

        self.new_btn = tk.Button(
            btn_row,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.reset_to_start,
        )
        self.new_btn.grid(row=0, column=0, padx=18)

        self.finish_btn = tk.Button(
            btn_row,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.destroy,
        )
        self.finish_btn.grid(row=0, column=1, padx=18)

        self.on_show()

    def on_show(self):
        wrap = int(max(600, self.app.winfo_width() * 0.85)) if self.app.winfo_width() > 1 else 700
        self.body_lbl.config(wraplength=wrap)

        # (Still using placeholder values here)
        baseline = "___"
        shift = "___"

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("النتيجة: سلبي ESBL"))
            self.metrics_lbl.config(text=rtl(f"تردد خط الأساس: {baseline} MHz\nالانزياح: {shift} MHz"),
                                    font=FONTS.get("arabic_body", FONTS["body"]))
            self.body_lbl.config(
                text=rtl("الانزياح المرصود لا يتجاوز حد الكشف ولا يتوافق مع نشاط ESBL."),
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
            self.new_btn.config(text=rtl("اختبار جديد"), font=FONTS.get("arabic_button", FONTS["button"]))
            self.finish_btn.config(text=rtl("إنهاء"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Result: ESBL Negative")
            self.metrics_lbl.config(text=f"Baseline resonance: {baseline} MHz\nFrequency shift: {shift} MHz",
                                    font=FONTS["body"])
            self.body_lbl.config(
                text="The observed frequency shift does not exceed the detection threshold and is not consistent with ESBL activity.",
                font=FONTS["body"],
            )
            self.new_btn.config(text="NEW TEST", font=FONTS["button"])
            self.finish_btn.config(text="FINISH", font=FONTS["button"])
