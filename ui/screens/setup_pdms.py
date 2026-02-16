import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class SetupPDMSScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(8, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Set up PDMS Substrate" if app.lang != "ar" else rtl("تجهيز طبقة PDMS")
        body = (
            "Please place the PDMS substrate inside the sensor holder in the device.\n"
            "Once it is in place and the lid is closed, press NEXT."
            if app.lang != "ar"
            else rtl("يرجى وضع طبقة PDMS داخل حامل الحساس.\nعند إغلاق الغطاء، اضغط التالي.")
        )

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 18)
        )
        tk.Label(content, text=body, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["muted"],
                 justify="center", wraplength=800).grid(row=2, column=0, pady=(0, 28))

        tk.Button(
            content,
            text="NEXT" if app.lang != "ar" else rtl("التالي"),
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=lambda: app.show("preheat"),
        ).grid(row=3, column=0, pady=10)
