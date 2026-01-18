import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 115200

CANDIDATES = [
    b"version\n",
    b"help\n",
    b"?\n",
    b"info\n",
    b"scan 1000000 10000000\n",   # small sweep just to see if accepted
    b"sweep\n",
    b"frequencies\n",
    b"data 0\n",
    b"data 1\n",
]

def read_some(s: serial.Serial, seconds: float = 0.6) -> bytes:
    end = time.time() + seconds
    out = bytearray()
    while time.time() < end:
        chunk = s.read(4096)
        if chunk:
            out += chunk
        else:
            time.sleep(0.05)
    return bytes(out)

with serial.Serial(PORT, BAUD, timeout=0.2) as s:
    time.sleep(0.2)
    s.reset_input_buffer()
    s.reset_output_buffer()

    # Wake it up
    s.write(b"\r\n")
    time.sleep(0.2)
    print("=== Initial read ===")
    print(read_some(s).decode(errors="replace"))

    for cmd in CANDIDATES:
        print("\n=== Sending:", cmd.decode(errors="replace").strip(), "===")
        s.write(cmd)
        time.sleep(0.2)
        resp = read_some(s)
        print(resp.decode(errors="replace") if resp else "(no response)")
