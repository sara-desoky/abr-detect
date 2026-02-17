# ui/rtl.py

def rtl(text: str) -> str:
    """
    Proper Arabic shaping + RTL display for Tkinter.
    Requires:
      pip install arabic-reshaper python-bidi
    """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        # Without reshaping, Tkinter will show disconnected letters.
        return text
