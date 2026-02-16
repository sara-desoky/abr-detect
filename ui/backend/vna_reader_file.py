# ui/backend/vna_reader_file.py
import os
from typing import Optional

class VNAReaderFile:
    """
    Reads the last line of result_*.txt and extracts 'Corresponding A' (Hz).
    Expected: 'Corresponding A: <float>'
    Matches the format you shared. :contentReference[oaicite:1]{index=1}
    """
    def __init__(self, result_file_path: str):
        self.path = result_file_path
        self._last_line: Optional[str] = None

    def latest_resonance_hz(self) -> Optional[float]:
        if not os.path.isfile(self.path):
            return None

        try:
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        except Exception:
            return None

        if not lines:
            return None

        line = lines[-1]
        if line == self._last_line:
            return None
        self._last_line = line

        if "Corresponding A:" not in line:
            return None

        try:
            return float(line.split("Corresponding A:")[1].strip())
        except Exception:
            return None
