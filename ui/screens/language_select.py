# ui/screens/language_select.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class LanguageSelectScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(
            self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]
        )
        self.title_lbl.grid(row=1, column=0, pady=(0, 25))

        btn_frame = tk.Frame(self, bg=COLORS["bg"])
        btn_frame.grid(row=2, column=0)

        # Use SAME font for both so button heights match
        btn_font = FONTS["button"]

        self.en_btn = tk.Button(
            btn_frame,
            text="English",
            font=btn_font,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self._choose("en"),
        )
        self.en_btn.grid(row=0, column=0, padx=20, pady=(0, 14))

        self.ar_btn = tk.Button(
            btn_frame,
            text=rtl("العربية"),
            font=btn_font,  # same font -> consistent sizing
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self._choose("ar"),
        )
        self.ar_btn.grid(row=1, column=0, padx=20, pady=(0, 10))

        self.on_show()

    def _choose(self, lang: str):
        self.app.set_language(lang)
        self.app.go_from_language()

    def on_show(self):
        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("اختر اللغة"))
        else:
            self.title_lbl.config(text="Select Language")
