# ui/backend/stability.py
from collections import deque

class StabilityChecker:
    """
    Stable when we have N consecutive abs(freq[i]-freq[i-1]) < threshold_mhz.
    freq is in Hz.
    """
    def __init__(self, n_consecutive: int = 10, threshold_mhz: float = 0.06):
        self.n = int(n_consecutive)
        self.th = float(threshold_mhz)
        self._freq_mhz = deque(maxlen=self.n + 1)

    def reset(self):
        self._freq_mhz.clear()

    def update(self, freq_hz: float) -> bool:
        mhz = float(freq_hz) / 1e6
        self._freq_mhz.append(mhz)
        if len(self._freq_mhz) < self.n + 1:
            return False
        deltas = [abs(self._freq_mhz[i] - self._freq_mhz[i - 1]) for i in range(1, len(self._freq_mhz))]
        return all(d < self.th for d in deltas)

    def progress(self) -> tuple[int, int]:
        got = max(0, len(self._freq_mhz) - 1)
        return (min(got, self.n), self.n)
