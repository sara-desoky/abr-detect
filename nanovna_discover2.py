import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 115200
PROMPT = b"ch>"

def read_until_prompt(s: serial.Serial, timeout_s: float = 2.0) -> bytes:
    end = time.time() + timeout_s
    buf = bytearray()
    while time.time() < end:
        chunk = s.read(4096)
        if chunk:
            buf += chunk
            if PROMPT in buf:
                break
        else:
            time.sleep(0.02)
    return bytes(buf)

def send_cmd(s: serial.Serial, cmd: str, timeout_s: float = 2.0) -> str:
    # CRLF matters on many NanoVNA firmwares
    s.write(cmd.encode() + b"\r\n")
    time.sleep(0.05)
    out = read_until_prompt(s, timeout_s=timeout_s)
    return out.decode(errors="replace")

with serial.Serial(PORT, BAUD, timeout=0.1) as s:
    time.sleep(0.2)
    s.reset_input_buffer()
    s.reset_output_buffer()

    # get to prompt
    s.write(b"\r\n")
    time.sleep(0.1)
    print("=== Initial ===")
    print(read_until_prompt(s, timeout_s=2.0).decode(errors="replace"))

    for cmd in ["help", "version", "info", "scan 1000000 10000000 101", "frequencies", "data 0"]:
        print(f"\n=== {cmd} ===")
        print(send_cmd(s, cmd, timeout_s=3.0))
