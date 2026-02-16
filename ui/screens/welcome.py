# ui/screens/welcome.py
import tkinter as tk
from ui.config import COLORS, FONTS


def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(6, weight=1)
        content.grid_columnconfigure(0, weight=1)

        if self.app.lang == "ar":
            title_text = rtl("مرحبًا")
            body_text = rtl("اضغط على بدء لاستخدام الجهاز.")
            btn_text = rtl("بدء")
            btn_font = FONTS.get("button_ar", FONTS["button"])
        else:
            title_text = "Welcome!"
            body_text = "Click Start to begin using the device."
            btn_text = "START"
            btn_font = FONTS["button"]

        title = tk.Label(
            content,
            text=title_text,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        )
        title.grid(row=1, column=0, pady=(0, 18))

        body = tk.Label(
            content,
            text=body_text,
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS.get("muted", "#666666"),
            justify="center",
        )
        body.grid(row=2, column=0, pady=(0, 28))

        btn_start = tk.Button(
            content,
            text=btn_text,
            font=btn_font,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self._on_start,
        )
        btn_start.grid(row=3, column=0, pady=10)

    def _on_start(self):
        # TODO: replace with your next real screen later
        self.app.show("preheat")
