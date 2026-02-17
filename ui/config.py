# ui/config.py

APP_TITLE = "ABR-DETECT"

WINDOW_W = 800
WINDOW_H = 480

COLORS = {
    "bg": "#FFFFFF",
    "text": "#111111",
    "muted": "#666666",

    "accent": "#1E7A3B",
    "accent_blue": "#1C2E7A",

    "success": "#1E7A3B",
    "danger": "#C04A3A",

    "btn_bg": "#DDEFD6",
    "btn_text": "#111111",

    "btn_disabled_bg": "#E9E9E9",
    "btn_disabled_text": "#A0A0A0",
}


FONTS = {
    "title": ("Times New Roman", 28, "bold"),
    "button": ("Times New Roman", 22, "bold"),
    "body": ("Arial", 16),
    "small": ("Arial", 12),

    # ✅ Arabic-capable font (must exist on your Pi)
    "button_ar": ("Noto Naskh Arabic", 22, "bold"),
    "title_ar": ("Noto Naskh Arabic", 28, "bold"),
    "body_ar": ("Noto Naskh Arabic", 16),
}

LOGO_PATH = "ui/assets/logo.png"
