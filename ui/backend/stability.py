# ui/backend/stability.py

class StabilityChecker:
    """
    Anchor-based stability:
      - First point becomes anchor
      - Each next point must satisfy |current - anchor| < threshold_mhz
      - If pass: count += 1
      - If fail: anchor = current, count = 0
      - Stable when count >= n_consecutive
    freq input is Hz; threshold is MHz.
    """
    def __init__(self, n_consecutive: int = 10, threshold_mhz: float = 0.06):
        self.n = int(n_consecutive)
        self.th_mhz = float(threshold_mhz)
        self.reset()

    def reset(self):
        self.anchor_mhz = None
        self.count = 0

    def update(self, freq_hz: float) -> bool:
        cur_mhz = float(freq_hz) / 1e6

        if self.anchor_mhz is None:
            self.anchor_mhz = cur_mhz
            self.count = 0
            return False

        if abs(cur_mhz - self.anchor_mhz) < self.th_mhz:
            self.count += 1
        else:
            self.anchor_mhz = cur_mhz
            self.count = 0

        return self.count >= self.n

    def progress(self) -> tuple[int, int]:
        return (min(self.count, self.n), self.n)
