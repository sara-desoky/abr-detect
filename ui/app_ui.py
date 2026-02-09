# ui/app_ui.py
import tkinter as tk
from ui.config import APP_TITLE, WINDOW_W, WINDOW_H, COLORS
from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen

class ABRDetectUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.configure(bg=COLORS["bg"])

        # container holds all screens stacked on top of each other
        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        self.lang = "en"  # default language

        self.screens = {}
        self.register_screens()
        self.show("language")

    def register_screens(self):
        self.screens["language"] = LanguageSelectScreen(self.container, self)
        self.screens["welcome"] = WelcomeScreen(self.container, self)

        for s in self.screens.values():
            s.grid(row=0, column=0, sticky="nsew")

    def show(self, name: str):
        self.screens[name].tkraise()
