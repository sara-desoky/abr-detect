# ui/rtl.py
def rtl(text: str, enabled: bool = True) -> str:
    """
    Returns Arabic-shaped + bidi-correct text for Tkinter.
    If libraries aren't installed, falls back to raw text.
    """
    if not enabled:
        return text

    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text
