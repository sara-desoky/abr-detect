# ui/backend/sim_devices.py
import time
import random

class SimArduino:
    def __init__(self, start_temp: float = 22.0):
        self.t = float(start_temp)
        self.target = 25.0
        self.enabled = False

    def start(self, target_c: float):
        self.target = float(target_c)
        self.enabled = True
        return ("SIM SETT OK", "SIM START OK")

    def stop(self):
        self.enabled = False
        return "SIM STOP OK"

    def status(self):
        if self.enabled:
            self.t += (self.target - self.t) * 0.08  # approach target
        noise = random.uniform(-0.05, 0.05)
        t2 = self.t + noise
        return {"t2": t2, "is_locked": True, "is_ready": abs(t2 - self.target) < 0.2, "raw": "SIM"}

class SimVNA:
    """
    Produces resonance readings that start noisy and then become stable.
    """
    def __init__(self):
        self.t0 = time.time()
        self.base = 731.050e6

    def latest_resonance_hz(self):
        elapsed = time.time() - self.t0

        if elapsed < 10:
            jitter = random.uniform(-250_000, 250_000)
        elif elapsed < 25:
            jitter = random.uniform(-90_000, 90_000)
        else:
            # stable enough that consecutive deltas often fall under 60kHz (0.06 MHz)
            jitter = random.uniform(-40_000, 40_000)

        return self.base + jitter
