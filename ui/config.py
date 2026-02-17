# ui/config.py

APP_TITLE = "ABR Detect"
WINDOW_W = 800
WINDOW_H = 480

COLORS = {
    "bg": "#FFFFFF",
    "text": "#111111",
    "muted": "#666666",

    # Accents (match your mockups)
    "accent": "#1E7A3B",        # green
    "accent_blue": "#1F3A93",   # navy/blue for “in progress…”
    "danger": "#D6453D",        # red for heating in progress
    "success": "#1E7A3B",       # green for success

    # Buttons
    "btn_bg": "#DDEFD6",
    "btn_text": "#111111",
    "btn_disabled_bg": "#D9D9D9",
    "btn_disabled_text": "#888888",

    # Card/border (optional)
    "border": "#222222",
}

FONTS = {
    "title": ("Times New Roman", 44, "bold"),
    "subtitle": ("Times New Roman", 28, "bold"),
    "button": ("Times New Roman", 30, "bold"),
    "body": ("Arial", 24),
    "small": ("Arial", 18),
    # If you install Arabic shaping libs + have a good Arabic font:
    "arabic_body": ("Noto Naskh Arabic", 24),
    "arabic_button": ("Noto Naskh Arabic", 30, "bold"),
}
