# ui/screens/load_processed_sample.py
import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl


class LoadProcessedSampleScreen(tk.Frame):
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

        self.title_lbl = tk.Label(content, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(row=1, column=0, pady=(0, 14))

        self.body_lbl = tk.Label(
            content,
            text="",
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
            wraplength=820,
        )
        self.body_lbl.grid(row=2, column=0, pady=(0, 18), padx=40)

        self.next_btn = tk.Button(
            content,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=18,
            height=2,
            command=self.app.confirm_sample_loaded,
        )
        self.next_btn.grid(row=3, column=0, pady=10)

        self.on_show()

    def on_show(self):
        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("أدخل العينة المعالجة"), font=FONTS["title"])
            self.body_lbl.config(
                text=rtl(
                    "باستخدام المحقنة المقدمة، أضف ٩٠ ميكرولتر من عينة البول المعالجة إلى خزان العينة.\n\n"
                    "تأكد أن غشاء PDMS يبقى سليمًا ويغطي الخزان الدائري بالكامل أثناء الحقن."
                ),
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
            self.next_btn.config(text=rtl("التالي"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Load Processed Sample", font=FONTS["title"])
            self.body_lbl.config(
                text=(
                    "Using the provided syringe, dispense 90 µL of the\n"
                    "processed urine sample into the sample reservoir.\n\n"
                    "Ensure the PDMS membrane remains intact and\n"
                    "fully covers the circular reservoir during injection."
                ),
                font=FONTS["body"],
            )
            self.next_btn.config(text="NEXT", font=FONTS["button"])
