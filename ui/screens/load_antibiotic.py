# ui/screens/load_antibiotic.py
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

        if app.lang == "ar":
            title = rtl("أضف المضاد الحيوي")
            body = rtl(
                "باستخدام محقنة ١٠٠ ميكرولتر، أضف ١٠ ميكرولتر من محلول المضاد الحيوي إلى خزان العينة.\n\n"
                "تأكد أن غشاء PDMS يبقى سليمًا ويغطي الخزان الدائري بالكامل أثناء الحقن."
            )
            btn = rtl("التالي")
            btn_font = FONTS.get("button_ar", FONTS["button"])
        else:
            title = "Load Antibiotic"
            body = (
                "Using the 100µL syringe, dispense 10 µL of the\n"
                "antibiotic solution into the sample reservoir.\n\n"
                "Ensure the PDMS membrane remains intact and\n"
                "fully covers the circular reservoir during injection."
            )
            btn = "NEXT"
            btn_font = FONTS["button"]

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 14)
        )
        tk.Label(
            content,
            text=body,
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        ).grid(row=2, column=0, pady=(0, 18), padx=40)

        tk.Button(
            content,
            text=btn,
            font=btn_font,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=self.app.confirm_antibiotic_loaded,
        ).grid(row=3, column=0, pady=10)
