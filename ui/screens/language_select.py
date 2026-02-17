# ui/screens/language_select.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class LanguageSelectScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)
        content.grid_columnconfigure(0, weight=1)

        tk.Label(
            content,
            text=f"Select Language | {rtl('اختر اللغة')}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).grid(row=1, column=0, pady=(0, 20))

        tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=lambda: self._choose("en"),
        ).grid(row=2, column=0, pady=10)

        tk.Button(
            content,
            text=rtl("العربية"),
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=lambda: self._choose("ar"),
        ).grid(row=3, column=0, pady=10)

    def _choose(self, lang: str):
        # IMPORTANT: this must rebuild screens so language applies everywhere
        self.app.set_language(lang)
        self.app.go_from_language()
