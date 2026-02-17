# ui/screens/result_screen.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class ResultScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew", padx=40, pady=20)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)

        self.title_lbl = tk.Label(content, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 16))

        self.metrics_lbl = tk.Label(content, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.metrics_lbl.grid(row=2, column=0, pady=(0, 14))

        self.body_lbl = tk.Label(content, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], justify="center")
        self.body_lbl.grid(row=3, column=0, pady=(0, 18))

        btn_row = tk.Frame(content, bg=COLORS["bg"])
        btn_row.grid(row=4, column=0, pady=(0, 10))

        self.new_test_btn = tk.Button(
            btn_row,
            font=FONTS["button_small"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.reset_to_start,
        )
        self.new_test_btn.grid(row=0, column=0, padx=10)

        self.finish_btn = tk.Button(
            btn_row,
            font=FONTS["button_small"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.reset_to_start,
        )
        self.finish_btn.grid(row=0, column=1, padx=10)

        self.on_show()

    def _wrap(self) -> int:
        w = self.winfo_toplevel().winfo_width()
        if w <= 1:
            w = self.winfo_toplevel().winfo_screenwidth()
        return int(w * 0.80)

    def on_show(self):
        self.body_lbl.config(wraplength=self._wrap())

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("النتيجة: سلبي (ESBL)"))
            self.metrics_lbl.config(text=rtl("تردد خط الأساس: ___ MHz\nإزاحة التردد: ___ MHz"))
            self.body_lbl.config(text=rtl("إزاحة التردد المرصودة لا تتجاوز حد الكشف ولا تتوافق مع نشاط ESBL."))
            self.new_test_btn.config(text=rtl("اختبار جديد"))
            self.finish_btn.config(text=rtl("إنهاء"))
        else:
            self.title_lbl.config(text="Result: ESBL Negative")
            self.metrics_lbl.config(text="Baseline resonance: ___ MHz\nFrequency shift: ___ MHz")
            self.body_lbl.config(
                text="The observed frequency shift does not exceed the detection threshold and is not consistent with ESBL activity."
            )
            self.new_test_btn.config(text="NEW TEST")
            self.finish_btn.config(text="FINISH")
