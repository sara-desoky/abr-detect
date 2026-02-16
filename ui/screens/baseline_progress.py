# ui/screens/baseline_progress.py
import tkinter as tk
from tkinter import ttk
import time
import threading
from ui.config import COLORS, FONTS

def rtl(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except Exception:
        return text

class BaselineProgressScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self._timer_thread = None
        self._timer_stop = threading.Event()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=COLORS["bg"])
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(8, weight=1)
        content.grid_columnconfigure(0, weight=1)

        if self.app.lang == "ar":
            title = rtl("قياس خط الأساس")
            body = rtl("جارٍ جمع بيانات خط الأساس...")
        else:
            title = "Baseline Measurement"
            body = "Collecting baseline data..."

        tk.Label(content, text=title, font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]).grid(
            row=1, column=0, pady=(0, 14)
        )
        tk.Label(content, text=body, font=FONTS.get("body", ("Arial", 16)),
                 bg=COLORS["bg"], fg=COLORS.get("muted", "#666666")).grid(row=2, column=0, pady=(0, 12))

        self.bar = ttk.Progressbar(content, length=600, mode="determinate", maximum=100)
        self.bar.grid(row=3, column=0, pady=(10, 10))

        self.time_lbl = tk.Label(content, text="--:--", font=FONTS.get("body", ("Arial", 18, "bold")),
                                 bg=COLORS["bg"], fg=COLORS["text"])
        self.time_lbl.grid(row=4, column=0, pady=(0, 10))

        self.freq_lbl = tk.Label(content, text="Current resonance: -- MHz",
                                 font=FONTS.get("body_small", ("Arial", 14)),
                                 bg=COLORS["bg"], fg=COLORS["text"])
        self.freq_lbl.grid(row=5, column=0, pady=(0, 10))

    def set_freq(self, freq_hz):
        if freq_hz is None:
            self.freq_lbl.config(text="Current resonance: -- MHz")
        else:
            self.freq_lbl.config(text=f"Current resonance: {freq_hz/1e6:.3f} MHz")

    def start_countdown(self, total_seconds: int):
        # stop any old timer
        self._timer_stop.set()
        self._timer_stop = threading.Event()

        def run():
            t0 = time.time()
            while not self._timer_stop.is_set():
                elapsed = int(time.time() - t0)
                remain = max(0, total_seconds - elapsed)
                pct = 100.0 * (elapsed / total_seconds) if total_seconds else 100.0

                mm = remain // 60
                ss = remain % 60

                def ui():
                    self.bar["value"] = max(0, min(100, pct))
                    self.time_lbl.config(text=f"{mm:02d}:{ss:02d}")

                self.app.after(0, ui)

                if remain <= 0:
                    break
                time.sleep(0.25)

        self._timer_thread = threading.Thread(target=run, daemon=True)
        self._timer_thread.start()
