import subprocess
import time

# Inputs to send
inputs = [
    "2.7",   # CPI
    "4.4",   # Unemployment
    "50000", # NFP
    "4.3",   # GDP Growth
    "2.8",   # Core PCE
    "0.0",   # Retail Sales
    "89.1"   # Consumer Confidence
]

input_str = "\n".join(inputs) + "\n"

print("Starting bot with automated inputs...")
process = subprocess.Popen(
    ['python', 'Version 1.1.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

stdout, stderr = process.communicate(input=input_str)

print("\n--- STDOUT ---")
print(stdout)
print("\n--- STDERR ---")
print(stderr)
