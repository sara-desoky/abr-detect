import tkinter as tk
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class LoadAntibioticScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(10, weight=1)
        content.grid_columnconfigure(0, weight=1)

        title = "Load Antibiotic" if app.lang != "ar" else rtl("إضافة المضاد")
        body = (
            "Using the syringe, dispense the antibiotic solution into the sample reservoir.\n\n"
            "Press NEXT when done."
            if app.lang != "ar"
            else rtl("باستخدام المحقنة، أضف محلول المضاد إلى الخزان.\n\nاضغط التالي عند الانتهاء.")
        )

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 14)
        )
        tk.Label(content, text=body, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["muted"],
                 justify="center", wraplength=850).grid(row=2, column=0, pady=(0, 22))

        tk.Button(
            content,
            text="NEXT" if app.lang != "ar" else rtl("التالي"),
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self.app.confirm_antibiotic_loaded,
        ).grid(row=3, column=0, pady=10)
