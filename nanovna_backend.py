from __future__ import annotations
import time
import math
import serial
from dataclasses import dataclass
from typing import List

PROMPT = b"ch>"

@dataclass
class ResonanceResult:
    freqs_hz: List[float]
    mag_db: List[float]
    f_res_hz: float

class NanoVNA:
    def __init__(self, port: str = "/dev/ttyACM0", baud: int = 115200):
        self.port = port
        self.baud = baud
        self.s: serial.Serial | None = None

    def __enter__(self) -> "NanoVNA":
        self.s = serial.Serial(self.port, self.baud, timeout=0.1)
        time.sleep(0.2)
        self.s.reset_input_buffer()
        self.s.reset_output_buffer()
        # wake prompt
        self._write(b"\r\n")
        self._read_until_prompt(timeout_s=2.0)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.s:
            self.s.close()
        self.s = None

    def _write(self, bts: bytes):
        assert self.s is not None
        self.s.write(bts)

    def _read_until_prompt(self, timeout_s: float = 2.0) -> bytes:
        assert self.s is not None
        end = time.time() + timeout_s
        buf = bytearray()
        while time.time() < end:
            chunk = self.s.read(4096)
            if chunk:
                buf += chunk
                if PROMPT in buf:
                    break
            else:
                time.sleep(0.02)
        return bytes(buf)

    def cmd(self, text: str, timeout_s: float = 2.0) -> str:
        # NanoVNA shell expects CRLF
        self._write(text.encode() + b"\r\n")
        time.sleep(0.05)
        out = self._read_until_prompt(timeout_s=timeout_s)
        return out.decode(errors="replace")

    def scan(self, start_hz: int, stop_hz: int, points: int) -> None:
        self.cmd(f"scan {start_hz} {stop_hz} {points}", timeout_s=2.0)

    def frequencies(self) -> List[float]:
        out = self.cmd("frequencies", timeout_s=3.0)
        freqs: List[float] = []
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("frequ") or line == "ch>":
                continue
            try:
                freqs.append(float(line))
            except ValueError:
                pass
        return freqs

    def data0_re_im(self) -> List[tuple[float, float]]:
        out = self.cmd("data 0", timeout_s=3.0)
        pairs: List[tuple[float, float]] = []
        for line in out.splitlines():
            line = line.strip()
            if not line or line.startswith("data") or line == "ch>":
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    re = float(parts[0])
                    im = float(parts[1])
                    pairs.append((re, im))
                except ValueError:
                    pass
        return pairs


def resonance_from_scan(
    port: str = "/dev/ttyACM0",
    start_hz: int = 1_000_000,
    stop_hz: int = 10_000_000,
    points: int = 101,
) -> ResonanceResult:
    """
    Resonance = frequency at minimum |S11| (deepest dip).
    We compute |S11| from (Re, Im) returned by `data 0`.
    """
    with NanoVNA(port=port) as vna:
        vna.scan(start_hz, stop_hz, points)
        freqs = vna.frequencies()
        data = vna.data0_re_im()

    n = min(len(freqs), len(data))
    freqs = freqs[:n]
    data = data[:n]

    mag_db: List[float] = []
    for re, im in data:
        mag = math.sqrt(re * re + im * im)
        mag = max(mag, 1e-12)
        mag_db.append(20.0 * math.log10(mag))

    idx = min(range(n), key=lambda i: mag_db[i])
    f_res = freqs[idx]

    return ResonanceResult(freqs_hz=freqs, mag_db=mag_db, f_res_hz=f_res)


def classify_esbl(f5_hz: float, f15_hz: float, threshold_hz: float) -> tuple[str, float]:
    shift = f15_hz - f5_hz
    label = "ESBL Positive" if shift > threshold_hz else "ESBL Negative"
    return label, shift
