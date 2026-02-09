# ui/screens/language_select.py
import tkinter as tk
from PIL import Image, ImageTk
from ui.config import COLORS, FONTS, LOGO_PATH

# --- Arabic shaping / RTL helper ---
def rtl(text: str) -> str:
    """
    Shapes Arabic and fixes RTL display for Tkinter.
    Requires: arabic-reshaper + python-bidi (optional).
    Falls back gracefully if unavailable.
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
        self.logo_img = None

        # ---------- Centered content block ----------
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(expand=True)

        # ---------- Title ----------
        title = tk.Label(
            content,
            text=f"Select Language | {rtl('اختر اللغة')}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        title.pack(pady=(0, 28))

        # ---------- English button ----------
        btn_en = tk.Button(
            content,
            text="English",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self.set_lang("en"),
        )
        btn_en.pack(pady=12)

        # ---------- Arabic button ----------
        btn_ar = tk.Button(
            content,
            text=rtl("عربي"),
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: self.set_lang("ar"),
        )
        btn_ar.pack(pady=12)

        # ---------- Logo ----------
        self._load_logo()

    def set_lang(self, lang):
        self.app.lang = lang
        self.app.show("welcome")

    def _load_logo(self):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((120, 45))
            self.logo_img = ImageTk.PhotoImage(img)  # keep reference!
            logo = tk.Label(self, image=self.logo_img, bg=COLORS["bg"])
            logo.place(x=20, rely=1.0, y=-20, anchor="sw")
        except Exception as e:
            print("Logo load failed:", e)
            logo = tk.Label(
                self,
                text="ABR DETECT",
                bg=COLORS["bg"],
                fg=COLORS["muted"],
                font=FONTS["small"],
            )
            logo.place(x=20, rely=1.0, y=-20, anchor="sw")
