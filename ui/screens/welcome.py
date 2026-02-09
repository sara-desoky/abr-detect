# ui/screens/welcome.py
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


class WelcomeScreen(tk.Frame):
    CONTENT_W = 560

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.logo_img = None

        # 3x3 grid so content always centers
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Center content block
        content = tk.Frame(self, bg=COLORS["bg"], width=self.CONTENT_W)
        content.grid(row=1, column=1)
        content.grid_propagate(False)

        content.grid_columnconfigure(0, weight=1)

        # Language strings
        if self.app.lang == "ar":
            title_text = rtl("مرحبًا")
            body_text = rtl("اضغط على بدء لاستخدام الجهاز.")
            btn_text = rtl("بدء")
            btn_font = FONTS.get("button_ar", FONTS["button"])
        else:
            title_text = "Welcome!"
            body_text = "Click Start to begin using the device."
            btn_text = "START"
            btn_font = FONTS["button"]

        title = tk.Label(
            content,
            text=title_text,
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            anchor="center",
            justify="center",
        )
        title.grid(row=0, column=0, pady=(0, 18), sticky="ew")

        body = tk.Label(
            content,
            text=body_text,
            font=FONTS.get("body", ("Arial", 16)),
            bg=COLORS["bg"],
            fg=COLORS.get("muted", "#666666"),
            justify="center",
            wraplength=self.CONTENT_W,
        )
        body.grid(row=1, column=0, pady=(0, 28), sticky="ew")

        btn_start = tk.Button(
            content,
            text=btn_text,
            font=btn_font,
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            activebackground=COLORS["btn_bg"],
            activeforeground=COLORS["btn_text"],
            relief="groove",
            borderwidth=2,
            command=self._on_start,
        )
        btn_start.grid(row=2, column=0, pady=12, sticky="ew")
        btn_start.config(padx=20, pady=10)

        self._load_logo()

    def _on_start(self):
        # TODO: change to your real next screen later
        self.app.show("language")

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
