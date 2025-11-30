from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import pyotp
import time

app = FastAPI()

# ------------------------------
# Models for API requests
# ------------------------------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

# ------------------------------
# Endpoint 1: POST /decrypt-seed
# ------------------------------
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: DecryptSeedRequest):
    try:
        # Load private key
        with open("student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        
        # Base64 decode
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        
        # Decrypt using RSA/OAEP-SHA256
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Convert to hex string
        decrypted_seed = decrypted_bytes.decode("utf-8").strip()
        
        # Validate 64-character hex
        if len(decrypted_seed) != 64 or not all(c in "0123456789abcdef" for c in decrypted_seed.lower()):
            raise ValueError("Invalid seed format")
        
        # Save to /data/seed.txt
        os.makedirs("/data", exist_ok=True)
        with open("/data/seed.txt", "w") as f:
            f.write(decrypted_seed)
        
        return {"status": "ok"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

# ------------------------------
# Endpoint 2: GET /generate-2fa
# ------------------------------
@app.get("/generate-2fa")
def generate_2fa():
    seed_file = "/data/seed.txt"
    if not os.path.exists(seed_file):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    with open(seed_file, "r") as f:
        hex_seed = f.read().strip()
    
    # Convert hex seed to base32
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    valid_for = 30 - (int(time.time()) % 30)  # Remaining seconds in current period
    
    return {"code": code, "valid_for": valid_for}

# ------------------------------
# Endpoint 3: POST /verify-2fa
# ------------------------------
@app.post("/verify-2fa")
def verify_2fa(request: Verify2FARequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")
    
    seed_file = "/data/seed.txt"
    if not os.path.exists(seed_file):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    with open(seed_file, "r") as f:
        hex_seed = f.read().strip()
    
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(base32_seed)
    
    valid = totp.verify(request.code, valid_window=1)  # ±30 seconds tolerance
    return {"valid": valid}
