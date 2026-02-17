# ui/screens/welcome.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 20))

        self.body_lbl = tk.Label(
            self, text="", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"],
            justify="center"
        )
        self.body_lbl.grid(row=2, column=0, padx=40, pady=(0, 30))

        self.start_btn = tk.Button(
            self,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self.app.go_from_welcome,   # ✅ THIS was the issue
        )
        self.start_btn.grid(row=3, column=0, pady=10)

        self.on_show()

    def on_show(self):
        wrap = int(max(600, self.app.winfo_width() * 0.85)) if self.app.winfo_width() > 1 else 700

        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("مرحباً"))
            self.body_lbl.config(text=rtl("أهلاً بك في جهاز ABR Detect.\nاضغط ابدأ لبدء الاختبار."), wraplength=wrap,
                                 font=FONTS.get("arabic_body", FONTS["body"]))
            self.start_btn.config(text=rtl("ابدأ"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Welcome")
            self.body_lbl.config(text="Welcome to ABR Detect.\nPress START to begin the test.", wraplength=wrap,
                                 font=FONTS["body"])
            self.start_btn.config(text="START", font=FONTS["button"])
