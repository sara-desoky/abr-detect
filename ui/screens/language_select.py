# ui/screens/language_select.py
import tkinter as tk
from PIL import Image, ImageTk
from ui.config import COLORS, FONTS, LOGO_PATH


def rtl(text: str) -> str:
    """
    Shapes Arabic and fixes RTL display for Tkinter.
    Optional deps: arabic-reshaper + python-bidi
    Falls back safely if not installed.
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

        # Make this frame expand to fill its grid cell
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Centered content block
        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")

        # Use grid inside content to center vertically & horizontally
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Title (fill X so it truly centers)
        title = tk.Label(
            content,
            text=f"Select Language | {rtl('اختر اللغة')}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        )
        title.grid(row=1, column=0, pady=(0, 28), sticky="ew")

        # English button
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
        btn_en.grid(row=2, column=0, pady=12)

        # Arabic button (shaped + optional Arabic font)
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
        btn_ar.grid(row=3, column=0, pady=12)

        # Bottom-left logo (anchored to bottom of this full-screen frame)
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
            logo.place(x=20, rely=1.0, y=-15, anchor="sw")
        except Exception as e:
            print("Logo load failed:", e)
            logo = tk.Label(
                self,
                text="ABR DETECT",
                bg=COLORS["bg"],
                fg=COLORS["muted"],
                font=FONTS.get("small", ("Arial", 12)),
            )
            logo.place(x=20, rely=1.0, y=-15, anchor="sw")
