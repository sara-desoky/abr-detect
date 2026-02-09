# ui/screens/language_select.py
import tkinter as tk
from PIL import Image, ImageTk
from ui.config import COLORS, FONTS, LOGO_PATH


def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


class LanguageSelectScreen(tk.Frame):
    CONTENT_W = 560  # tweak 520–600

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.logo_img = None

        # --- 3x3 grid on the full screen frame ---
        # Put content in the middle cell so it ALWAYS centers
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # --- Center content block (fixed width) ---
        content = tk.Frame(self, bg=COLORS["bg"], width=self.CONTENT_W)
        content.grid(row=1, column=1)
        content.grid_propagate(False)  # do not shrink to text

        content.grid_columnconfigure(0, weight=1)

        # Title (fills width so centering is perfect)
        title = tk.Label(
            content,
            text=f"Select Language | {rtl('اختر اللغة')}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        )
        title.grid(row=0, column=0, pady=(0, 28), sticky="ew")

        # Buttons fill the content width
        btn_en = tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            relief="groove",
            borderwidth=2,
            command=lambda: self.set_lang("en"),
        )
        btn_en.grid(row=1, column=0, pady=12, sticky="ew")
        btn_en.config(padx=20, pady=10)

        btn_ar = tk.Button(
            content,
            text=rtl("عربي"),
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            relief="groove",
            borderwidth=2,
            command=lambda: self.set_lang("ar"),
        )
        btn_ar.grid(row=2, column=0, pady=12, sticky="ew")
        btn_ar.config(padx=20, pady=10)

        # Bottom-left logo
        self._load_logo()

    def set_lang(self, lang):
        self.app.lang = lang
        self.app.show("welcome")

    def _load_logo(self):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((207, 58), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo = tk.Label(self, image=self.logo_img, bg=COLORS["bg"])
            logo.place(x=20, rely=1.0, y=-15, anchor="sw")
        except Exception as e:
            print("Logo load failed:", e)
            logo = tk.Label(
                self,
                text="ABR DETECT",
                bg=COLORS["bg"],
                fg=COLORS.get("muted", "#666666"),
                font=FONTS.get("small", ("Arial", 12)),
            )
            logo.place(x=20, rely=1.0, y=-15, anchor="sw")
