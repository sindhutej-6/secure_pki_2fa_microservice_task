#!/usr/bin/env python3
import os
import base64
import time
import pyotp
from datetime import datetime

# Path to seed file
seed_file = "/data/seed.txt"

try:
    with open(seed_file, "r") as f:
        hex_seed = f.read().strip()
except FileNotFoundError:
    print(f"{datetime.utcnow():%Y-%m-%d %H:%M:%S} - Seed file not found")
    exit(1)

# Convert hex to base32
seed_bytes = bytes.fromhex(hex_seed)
base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

# Generate TOTP code
totp = pyotp.TOTP(base32_seed)
code = totp.now()

# UTC timestamp
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Print formatted output
print(f"{timestamp} - 2FA Code: {code}")
