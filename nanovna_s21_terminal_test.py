from __future__ import annotations

import argparse
import math
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple

import serial
from serial.tools import list_ports

PROMPT = b"ch>"
DEFAULT_BAUD = 115200


@dataclass
class SweepResult:
    freqs_hz: List[float]
    s21_mag_db: List[float]
    f_res_hz: float
    min_db: float


def list_serial_ports() -> List[str]:
    ports = [p.device for p in list_ports.comports()]
    return sorted(ports)


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
    s.write(cmd.encode("ascii") + b"\r\n")
    time.sleep(0.05)
    out = read_until_prompt(s, timeout_s=timeout_s)
    return out.decode(errors="replace")


def parse_frequencies(raw: str) -> List[float]:
    freqs: List[float] = []
    for line in raw.splitlines():
        t = line.strip()
        if not t or t == "ch>" or t.startswith("frequ"):
            continue
        try:
            freqs.append(float(t))
        except ValueError:
            pass
    return freqs


def parse_data_pairs(raw: str) -> List[Tuple[float, float]]:
    pairs: List[Tuple[float, float]] = []
    for line in raw.splitlines():
        t = line.strip()
        if not t or t == "ch>" or t.startswith("data"):
            continue
        parts = t.split()
        if len(parts) < 2:
            continue
        try:
            re = float(parts[0])
            im = float(parts[1])
            pairs.append((re, im))
        except ValueError:
            pass
    return pairs


def s21_resonance_from_scan(
    port: str,
    start_hz: int,
    stop_hz: int,
    points: int,
    baud: int = DEFAULT_BAUD,
) -> SweepResult:
    with serial.Serial(port, baud, timeout=0.1) as s:
        time.sleep(0.25)
        s.reset_input_buffer()
        s.reset_output_buffer()

        s.write(b"\r\n")
        initial = read_until_prompt(s, timeout_s=2.0)
        if PROMPT not in initial:
            raise RuntimeError(
                "Did not receive NanoVNA prompt 'ch>'. Check port/baud/cable and try again."
            )

        print("[cmd] scan", start_hz, stop_hz, points)
        send_cmd(s, f"scan {start_hz} {stop_hz} {points}", timeout_s=3.0)

        print("[cmd] frequencies")
        raw_freqs = send_cmd(s, "frequencies", timeout_s=3.0)

        print("[cmd] data 1   # S21 complex data")
        raw_data1 = send_cmd(s, "data 1", timeout_s=3.0)

    freqs = parse_frequencies(raw_freqs)
    s21_pairs = parse_data_pairs(raw_data1)

    n = min(len(freqs), len(s21_pairs))
    if n == 0:
        raise RuntimeError(
            "Parsed zero points from NanoVNA output. Try points=101 and check command support."
        )

    freqs = freqs[:n]
    s21_pairs = s21_pairs[:n]

    mag_db: List[float] = []
    for re, im in s21_pairs:
        mag = math.sqrt(re * re + im * im)
        mag = max(mag, 1e-12)
        mag_db.append(20.0 * math.log10(mag))

    idx_min = min(range(n), key=lambda i: mag_db[i])
    return SweepResult(
        freqs_hz=freqs,
        s21_mag_db=mag_db,
        f_res_hz=freqs[idx_min],
        min_db=mag_db[idx_min],
    )


def pick_port_or_fail(user_port: str | None) -> str:
    if user_port:
        return user_port

    ports = list_serial_ports()
    if not ports:
        raise RuntimeError("No serial ports found. Plug in NanoVNA and rerun.")

    print("Detected serial ports:", ", ".join(ports))
    if len(ports) == 1:
        print("Using only detected port:", ports[0])
        return ports[0]

    print("Multiple ports found. Pass --port COMx explicitly.")
    raise RuntimeError("Ambiguous serial port selection.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Terminal NanoVNA S21 resonance test (no UI/backend integration)."
    )
    parser.add_argument("--port", default=None, help="Serial port (example: COM6)")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    parser.add_argument("--start-hz", type=int, default=650_000_000)
    parser.add_argument("--stop-hz", type=int, default=820_000_000)
    parser.add_argument("--points", type=int, default=401)
    parser.add_argument(
        "--list-ports",
        action="store_true",
        help="Only print detected serial ports and exit.",
    )
    args = parser.parse_args()

    if args.list_ports:
        ports = list_serial_ports()
        print("Detected ports:")
        if ports:
            for p in ports:
                print(" -", p)
        else:
            print(" (none)")
        return 0

    try:
        port = pick_port_or_fail(args.port)
        result = s21_resonance_from_scan(
            port=port,
            start_hz=args.start_hz,
            stop_hz=args.stop_hz,
            points=args.points,
            baud=args.baud,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    print("\nS21 resonance sweep complete")
    print(f"Port: {port}")
    print(f"Sweep: {args.start_hz} Hz -> {args.stop_hz} Hz, points={args.points}")
    print(f"Estimated resonance (min |S21|): {result.f_res_hz:.2f} Hz")
    print(f"Depth at resonance: {result.min_db:.2f} dB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
