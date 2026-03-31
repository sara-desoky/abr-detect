import tkinter as tk

from ui.config import COLORS, FONTS
from ui.rtl import rtl


class ResultScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_lbl = tk.Label(
            self, text="", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["text"]
        )
        self.title_lbl.grid(row=1, column=0, pady=(0, 16))

        self.metrics_lbl = tk.Label(
            self,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        self.metrics_lbl.grid(row=2, column=0, pady=(0, 18))

        self.body_lbl = tk.Label(
            self,
            text="",
            font=FONTS["body"],
            bg=COLORS["bg"],
            fg=COLORS["text"],
            justify="center",
        )
        self.body_lbl.grid(row=3, column=0, padx=50, pady=(0, 22))

        btn_row = tk.Frame(self, bg=COLORS["bg"])
        btn_row.grid(row=4, column=0, pady=10)

        self.new_btn = tk.Button(
            btn_row,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.reset_to_start,
        )
        self.new_btn.grid(row=0, column=0, padx=18)

        self.finish_btn = tk.Button(
            btn_row,
            text="",
            font=FONTS["button"],
            bg=COLORS["btn_bg"],
            fg=COLORS["btn_text"],
            width=14,
            height=2,
            command=self.app.finish_and_quit,
        )
        self.finish_btn.grid(row=0, column=1, padx=18)

        self.on_show()

    def on_show(self):
        wrap = (
            int(max(600, self.app.winfo_width() * 0.85))
            if self.app.winfo_width() > 1
            else 700
        )
        self.body_lbl.config(wraplength=wrap)

        result = getattr(self.app, "latest_result", None) or {}
        label = result.get("label", "Insufficient Data")
        baseline_hz = result.get("baseline_hz")
        final_hz = result.get("final_hz")
        shift_hz = result.get("shift_hz")
        threshold_hz = result.get("threshold_hz", -30_000.0)
        mode = result.get("mode", "experiment")

        if mode == "simulation":
            target_value_en = "10 seconds"
            target_value_ar = "١٠ ثوانٍ"
        else:
            target_value_en = "12 min"
            target_value_ar = "١٢ دقيقة"

        baseline_txt = (
            f"{baseline_hz / 1e6:.6f}"
            if isinstance(baseline_hz, (int, float))
            else "N/A"
        )
        final_txt = (
            f"{final_hz / 1e6:.6f}" if isinstance(final_hz, (int, float)) else "N/A"
        )
        shift_khz_txt = (
            f"{shift_hz / 1e3:+.2f}" if isinstance(shift_hz, (int, float)) else "N/A"
        )

        clean_mode = getattr(self.app, "clean_mode", False)

        if self.app.lang == "ar":
            title_text = "النتيجة: سلبي" if label == "ESBL Negative" else "النتيجة: إيجابي"
            self.title_lbl.config(text=rtl(title_text))

            if clean_mode:
                self.metrics_lbl.config(text="", font=FONTS.get("arabic_body", FONTS["body"]))
                clean_body = (
                    "التحول الملحوظ في التردد لا يتجاوز حد الكشف ولا يتوافق مع نشاط ESBL."
                    if label == "ESBL Negative"
                    else "التحول الملحوظ في التردد يتجاوز حد الكشف ويتوافق مع نشاط ESBL."
                )
                self.body_lbl.config(
                    text=rtl(clean_body),
                    font=FONTS.get("arabic_body", FONTS["body"]),
                )
            else:
                self.metrics_lbl.config(
                    text=rtl(
                        f"تردد خط الأساس: {baseline_txt} MHz\n"
                        f"تردد الرنين بعد {target_value_ar}: {final_txt} MHz\n"
                        f"التحول: {shift_khz_txt} kHz"
                    ),
                    font=FONTS.get("arabic_body", FONTS["body"]),
                )
                self.body_lbl.config(
                    text=rtl(
                        f"المعيار: ESBL سلبي إذا كان التحول > {threshold_hz / 1e3:.0f} kHz."
                    ),
                    font=FONTS.get("arabic_body", FONTS["body"]),
                )

            self.new_btn.config(
                text=rtl("اختبار جديد"),
                font=FONTS.get("arabic_button", FONTS["button"]),
            )
            self.finish_btn.config(
                text=rtl("إنهاء"),
                font=FONTS.get("arabic_button", FONTS["button"]),
            )
            return

        self.title_lbl.config(text=f"Result: {label}")
        if clean_mode:
            self.metrics_lbl.config(text="", font=FONTS["body"])
            clean_body = (
                "The observed frequency shift doesn't exceed the detection threshold and is not consistent with ESBL activity."
                if label == "ESBL Negative"
                else "The observed frequency shift exceeds the detection threshold and is consistent with ESBL activity."
            )
            self.body_lbl.config(text=clean_body, font=FONTS["body"])
        else:
            self.metrics_lbl.config(
                text=(
                    f"Baseline resonance (pre-penG): {baseline_txt} MHz\n"
                    f"Resonance after {target_value_en}: {final_txt} MHz\n"
                    f"Frequency shift: {shift_khz_txt} kHz"
                ),
                font=FONTS["body"],
            )
            self.body_lbl.config(
                text=f"Decision rule: ESBL Negative if shift > {threshold_hz / 1e3:.0f} kHz.",
                font=FONTS["body"],
            )
        self.new_btn.config(text="NEW TEST", font=FONTS["button"])
        self.finish_btn.config(text="FINISH", font=FONTS["button"])
