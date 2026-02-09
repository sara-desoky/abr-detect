# ui/screens/welcome.py
import tkinter as tk
from ui.config import COLORS, FONTS

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(expand=True)

        title = tk.Label(content, text="Welcome!", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"])
        title.pack(pady=(0, 12))

        body = tk.Label(content, text="Click Start to begin using the device.", font=FONTS["body"],
                        bg=COLORS["bg"], fg=COLORS["text"])
        body.pack(pady=(0, 20))

        start = tk.Button(content, text="START", font=FONTS["button"], bg=COLORS["btn_bg"],
                          fg=COLORS["btn_text"], width=10, command=self.on_start)
        start.pack()

    def on_start(self):
        # later: go to PDMS step screen
        print("Start pressed")
