import tkinter as tk
from tkinter import ttk
import threading
import time

# ---- TEMP: mock backend (replace with NanoVNA later) ----
def run_protocol_mock(threshold_hz=1_000_000):
    f5 = 1.212e9
    f15 = 1.214e9
    shift = f15 - f5
    label = "ESBL Positive" if shift > threshold_hz else "ESBL Negative"
    return {
        "f_res_5_hz": f5,
        "f_res_15_hz": f15,
        "shift_hz": shift,
        "label": label,
    }

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ABR Detect")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomePage, StepPage, CollectPage, ResultPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.steps = [
            "1. Open the top lid",
            "2. Add buffer to the inlet",
            "3. Close the top lid",
            "4. Ready to begin data collection",
        ]

        self.step_index = 0
        self.results = None
        self.show_frame("WelcomePage")

    def show_frame(self, name):
        self.frames[name].tkraise()

    def start_steps(self):
        self.step_index = 0
        self.frames["StepPage"].set_step(self.steps[self.step_index])
        self.show_frame("StepPage")

    def next_step(self):
        self.step_index += 1
        if self.step_index < len(self.steps):
            self.frames["StepPage"].set_step(self.steps[self.step_index])
        else:
            self.show_frame("CollectPage")
            self.start_collection()

    def start_collection(self):
        collect = self.frames["CollectPage"]
        collect.set_status("Collecting data...")

        def worker():
            collect.set_status("Collecting 5 min data...")
            time.sleep(2)

            collect.set_status("Collecting 15 min data...")
            time.sleep(2)

            out = run_protocol_mock()
            self.after(0, lambda: self.show_results(out))

        threading.Thread(target=worker, daemon=True).start()

    def show_results(self, out):
        self.frames["ResultPage"].update_result(out)
        self.show_frame("ResultPage")


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="WELCOME", font=("Arial", 28)).pack(pady=30)
        ttk.Button(self, text="START", command=controller.start_steps)\
            .pack(ipadx=40, ipady=20)


class StepPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.step_text = tk.StringVar()
        ttk.Label(self, text="Instructions", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self, textvariable=self.step_text, font=("Arial", 18),
                  wraplength=760, justify="center").pack(pady=40)
        ttk.Button(self, text="NEXT", command=controller.next_step)\
            .pack(ipadx=40, ipady=15)

    def set_step(self, text):
        self.step_text.set(text)


class CollectPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.status = tk.StringVar(value="Waiting...")
        ttk.Label(self, text="Data Collection", font=("Arial", 22)).pack(pady=20)
        ttk.Label(self, textvariable=self.status, font=("Arial", 16)).pack(pady=10)
        self.pb = ttk.Progressbar(self, mode="indeterminate")
        self.pb.pack(fill="x", padx=40, pady=20)
        self.pb.start(10)

    def set_status(self, msg):
        self.status.set(msg)


class ResultPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.label = tk.StringVar()
        self.detail = tk.StringVar()

        ttk.Label(self, text="RESULT", font=("Arial", 22)).pack(pady=20)
        ttk.Label(self, textvariable=self.label, font=("Arial", 26)).pack(pady=10)
        ttk.Label(self, textvariable=self.detail, font=("Arial", 14)).pack(pady=10)
        ttk.Button(self, text="RESTART",
                   command=lambda: controller.show_frame("WelcomePage"))\
            .pack(ipadx=20, ipady=10)

    def update_result(self, out):
        self.label.set(out["label"])
        self.detail.set(
            f"Res @ 5 min: {out['f_res_5_hz']/1e6:.3f} MHz\n"
            f"Res @ 15 min: {out['f_res_15_hz']/1e6:.3f} MHz\n"
            f"Shift: {out['shift_hz']/1e6:.3f} MHz"
        )

if __name__ == "__main__":
    App().mainloop()
