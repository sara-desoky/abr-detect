from nanovna_backend import resonance_from_scan, classify_esbl
import time

PORT = "/dev/ttyACM0"

# Set your real sweep range for your sensor (edit these!)
START_HZ = 1_000_000
STOP_HZ  = 10_000_000
POINTS   = 101

THRESH_HZ = 1_000_000  # Example: 1 MHz threshold (change later)

print("Measuring '5 min' point NOW...")
r5 = resonance_from_scan(PORT, START_HZ, STOP_HZ, POINTS)
print("f_res_5 =", r5.f_res_hz)

print("Waiting 10 seconds (demo)...")
time.sleep(10)

print("Measuring '15 min' point NOW...")
r15 = resonance_from_scan(PORT, START_HZ, STOP_HZ, POINTS)
print("f_res_15 =", r15.f_res_hz)

label, shift = classify_esbl(r5.f_res_hz, r15.f_res_hz, THRESH_HZ)
print("SHIFT (Hz):", shift)
print("RESULT:", label)
