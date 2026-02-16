# ui/config.py

APP_TITLE = "ABR-DETECT"
WINDOW_W = 800
WINDOW_H = 480

COLORS = {
    "bg": "#FFFFFF",
    "text": "#111111",
    "muted": "#666666",

    # main accent (green)
    "accent": "#1E7A3B",

    # buttons
    "btn_bg": "#DDEFD6",
    "btn_text": "#111111",

    # Arabic text (if you want a separate color later)
    "arabic": "#111111",

    # ✅ needed by baseline_progress.py
    "accent_blue": "#1F3A73",       # blue heading
    "btn_disabled_bg": "#D9D9D9",   # greyed-out button bg
    "btn_disabled_text": "#888888", # greyed-out button text
}

FONTS = {
    "title": ("Times New Roman", 28, "bold"),
    "button": ("Times New Roman", 22, "bold"),
    "body": ("Arial", 16),
    "small": ("Arial", 12),
    # optional Arabic-specific override
    # "button_ar": ("Noto Naskh Arabic", 22, "bold"),
}

LOGO_PATH = "ui/assets/logo.png"
