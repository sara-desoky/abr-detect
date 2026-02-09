# ui/screens/language_select.py
import tkinter as tk
from PIL import Image, ImageTk
from ui.config import COLORS, FONTS, LOGO_PATH

class LanguageSelectScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.logo_img = None

        # Center content
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(expand=True)

        title = tk.Label(
            content,
            text="Select Language | اختر اللغة",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"]
        )
        title.pack(pady=(0, 20))

        btn_en = tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=1,
            command=lambda: self.set_lang("en")
        )
        btn_en.pack(pady=8)

        btn_ar = tk.Button(
            content,
            text="عربي",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=16,
            height=1,
            command=lambda: self.set_lang("ar")
        )
        btn_ar.pack(pady=8)

        # Bottom-left logo
        self.logo_label = tk.Label(self, bg=COLORS["bg"])
        self.logo_label.place(x=20, y=WINDOW_SAFE_BOTTOM(self))

        self._load_logo()

    def set_lang(self, lang):
        self.app.lang = lang
        self.app.show("welcome")

    def _load_logo(self):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((110, 40))  # tweak to match your Figma
            self.logo_img = ImageTk.PhotoImage(img)
            self.logo_label.config(image=self.logo_img)
            self.logo_label.place(x=20, y=self.winfo_reqheight()-60)
        except Exception as e:
            # If logo fails, app still runs
            self.logo_label.config(text="ABR DETECT", fg=COLORS["muted"])

def WINDOW_SAFE_BOTTOM(frame):
    # helper for initial placement before geometry exists
    return 400
