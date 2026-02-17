# ui/screens/language_select.py
import tkinter as tk
from ui.config import COLORS, FONTS


class LanguageSelectScreen(tk.Frame):
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

        tk.Label(content, text="Select Language", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 20)
        )

        tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self._choose("en"),
        ).grid(row=2, column=0, pady=(0, 12))

        tk.Button(
            content,
            text="العربية",
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self._choose("ar"),
        ).grid(row=3, column=0)

    def _choose(self, lang: str):
        self.app.set_language(lang)
        self.app.go_from_language()
