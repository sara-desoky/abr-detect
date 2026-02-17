# ui/config.py

APP_TITLE = "ABR Detect"
WINDOW_W = 800
WINDOW_H = 480

COLORS = {
    "bg": "#FFFFFF",
    "text": "#111111",
    "muted": "#666666",

    "accent": "#1E7A3B",
    "accent_blue": "#1F3A93",
    "danger": "#D6453D",

    "success": "#1E7A3B",
    "accent_green": "#1E7A3B",

    "btn_bg": "#DDEFD6",
    "btn_text": "#111111",
    "btn_disabled_bg": "#D9D9D9",
    "btn_disabled_text": "#888888",

    "border": "#222222",
}

# ✅ Reduced sizes to keep layout within 7" Pi screen (and prevent bottom buttons clipping)
FONTS = {
    "title": ("Times New Roman", 34, "bold"),
    "subtitle": ("Times New Roman", 22, "bold"),
    "button": ("Times New Roman", 24, "bold"),
    "body": ("Arial", 18),
    "small": ("Arial", 14),

    # Arabic (matching the same sizes)
    "arabic_body": ("Noto Naskh Arabic", 18),
    "arabic_button": ("Noto Naskh Arabic", 24, "bold"),
}
