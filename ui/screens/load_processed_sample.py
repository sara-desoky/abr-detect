# ui/screens/load_processed_sample.py
import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class LoadProcessedSampleScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(7, weight=1)
        content.grid_columnconfigure(0, weight=1)

        if self.app.lang == "ar":
            title = rtl("أدخل العينة المعالجة")
            body = rtl("باستخدام المحقنة، أدخل العينة المعالجة في الخزان.\n\nاضغط التالي عند الانتهاء.")
            btn = rtl("التالي")
            btn_font = FONTS.get("button_ar", FONTS["button"])
        else:
            title = "Load Processed Sample"
            body = "Using the syringe, inject the processed sample into the reservoir.\n\nPress NEXT when done."
            btn = "NEXT"
            btn_font = FONTS["button"]

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 14)
        )
        tk.Label(content, text=body, font=FONTS.get("body", ("Arial", 16)),
                 bg=COLORS["bg"], fg=COLORS.get("muted", "#666666"),
                 justify="center", wraplength=900).grid(row=2, column=0, pady=(0, 18))

        tk.Button(
            content,
            text=btn,
            font=btn_font,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self.app.confirm_sample_loaded,
        ).grid(row=3, column=0, pady=10)
