# ui/backend/arduino_serial.py
from typing import Optional
import time

try:
    import serial  # pyserial
except Exception:
    serial = None

class ArduinoSerial:
    """
    Requires Arduino sketch to accept:
      START
      STOP
      SETT <temp>
      STATUS -> STATUS,<t2>,<pwm_or_NA>,<isLocked 0/1>,<isReady 0/1>
    """
    def __init__(self, port: str, baud: int = 115200, timeout_s: float = 1.0):
        if serial is None:
            raise RuntimeError("pyserial not installed. Add 'pyserial' to requirements.txt")
        self.ser = serial.Serial(port, baudrate=baud, timeout=timeout_s)
        time.sleep(2.0)  # allow Arduino auto-reset
        self.flush()

    def flush(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send(self, line: str) -> str:
        self.ser.write((line.strip() + "\n").encode("utf-8"))
        self.ser.flush()
        return self.ser.readline().decode("utf-8", errors="ignore").strip()

    def start(self, target_c: float):
        r1 = self.send(f"SETT {target_c}")
        r2 = self.send("START")
        return (r1, r2)

    def stop(self):
        return self.send("STOP")

    def status(self) -> Optional[dict]:
        resp = self.send("STATUS")
        if not resp.startswith("STATUS,"):
            return None
        parts = resp.split(",")
        try:
            t2 = float(parts[1])
            is_locked = bool(int(parts[3]))
            is_ready = bool(int(parts[4]))
            return {"t2": t2, "is_locked": is_locked, "is_ready": is_ready, "raw": resp}
        except Exception:
            return None
