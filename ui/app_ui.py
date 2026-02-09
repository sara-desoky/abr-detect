import tkinter as tk
from ui.config import APP_TITLE, WINDOW_W, WINDOW_H, COLORS
from ui.screens.language_select import LanguageSelectScreen
from ui.screens.welcome import WelcomeScreen

class ABRDetectUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.configure(bg=COLORS["bg"])

        # Fullscreen on Pi (press Esc to exit fullscreen while testing)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.lang = "en"

        self.container = tk.Frame(self, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.screens = {}
        self.register_screens()
        self.show("language")

    def register_screens(self):
        self.screens["language"] = LanguageSelectScreen(self.container, self)
        self.screens["welcome"] = WelcomeScreen(self.container, self)

        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

    def show(self, name: str):
        self.screens[name].tkraise()
