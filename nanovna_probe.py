import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 115200

with serial.Serial(PORT, BAUD, timeout=1) as s:
    time.sleep(0.2)

    # Some NanoVNA firmwares respond to "help" or just echo/ignore.
    # We'll just try reading anything that comes back after sending a newline.
    s.write(b"\r\n")
    time.sleep(0.2)

    data = s.read(2000)
    print("RAW BYTES LEN:", len(data))
    if data:
        try:
            print(data.decode(errors="replace"))
        except Exception:
            print(data)
