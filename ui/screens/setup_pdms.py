import tkinter as tk
from ui.config import COLORS, FONTS
from ui.rtl import rtl

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

        self.title_lbl = tk.Label(content, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        self.title_lbl.grid(
            row=1, column=0, pady=(0, 18)
        )
        self.body_lbl = tk.Label(
            content,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            justify="center",
            wraplength=800,
        )
        self.body_lbl.grid(row=2, column=0, pady=(0, 28))

        self.next_btn = tk.Button(
            content,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=2,
            command=self.app.confirm_pdms_ready
        )
        self.next_btn.grid(row=3, column=0, pady=10)

        self.on_show()

    def on_show(self):
        if self.app.lang == "ar":
            self.title_lbl.config(text=rtl("تجهيز طبقة PDMS"), font=FONTS["title"])
            self.body_lbl.config(
                text=rtl("يرجى وضع طبقة PDMS داخل حامل الحساس.\nعند إغلاق الغطاء، اضغط التالي."),
                font=FONTS.get("arabic_body", FONTS["body"]),
            )
            self.next_btn.config(text=rtl("التالي"), font=FONTS.get("arabic_button", FONTS["button"]))
        else:
            self.title_lbl.config(text="Set up PDMS Substrate", font=FONTS["title"])
            self.body_lbl.config(
                text=(
                    "Please place the PDMS substrate inside the sensor holder in the device.\n"
                    "Once it is in place and the lid is closed, press NEXT."
                ),
                font=FONTS["body"],
            )
            self.next_btn.config(text="NEXT", font=FONTS["button"])
