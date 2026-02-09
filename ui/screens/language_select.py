# ui/screens/language_select.py
import tkinter as tk
from ui.config import COLORS, FONTS


def rtl(text: str) -> str:
    """
    Optional Arabic shaping + RTL (works if libs installed).
    Falls back to plain text if not installed.
    """
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

        # Fill the available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Center content (this was the clean version)
        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            content,
            text=f"Select Language | {rtl('اختر اللغة')}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        )
        title.grid(row=1, column=0, pady=(0, 20))

        btn_en = tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=lambda: self.set_lang("en"),
        )
        btn_en.grid(row=2, column=0, pady=10)

        btn_ar = tk.Button(
            content,
            text=rtl("عربي"),
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=lambda: self.set_lang("ar"),
        )
        btn_ar.grid(row=3, column=0, pady=10)

    def set_lang(self, lang):
        self.app.lang = lang
        self.app.show("welcome")
