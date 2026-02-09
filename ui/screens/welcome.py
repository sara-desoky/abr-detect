# ui/screens/welcome.py
import tkinter as tk
from PIL import Image, ImageTk
from ui.config import COLORS, FONTS, LOGO_PATH

# --- Arabic shaping / RTL helper ---
def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.logo_img = None

        # ---------- Centered content ----------
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(expand=True)

        # ---------- Title ----------
        title_text = (
            "Welcome!"
            if app.lang == "en"
            else rtl("مرحبًا")
        )

        title = tk.Label(
            content,
            text=title_text,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
        )
        title.pack(pady=(0, 20))

        # ---------- Body text ----------
        body_text = (
            "Click Start to begin using the device."
            if app.lang == "en"
            else rtl("اضغط على بدء لاستخدام الجهاز")
        )

        body = tk.Label(
            content,
            text=body_text,
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            justify="center",
        )
        body.pack(pady=(0, 28))

        # ---------- Start button ----------
        start_text = "START" if app.lang == "en" else rtl("بدء")

        btn_start = tk.Button(
            content,
            text=start_text,
            font=FONTS.get("button_ar", FONTS["button"]),
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            width=18,
            height=2,
            command=lambda: app.show("next_step"),  # adjust when you add next screen
        )
        btn_start.pack(pady=12)

        # ---------- Logo ----------
        self._load_logo()

    def _load_logo(self):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((120, 45))
            self.logo_img = ImageTk.PhotoImage(img)
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
