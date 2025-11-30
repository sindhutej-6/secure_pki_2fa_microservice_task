import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP
    
    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object
    
    Returns:
        Decrypted hex seed (64-character string)
    """
    # 1. Base64 decode the encrypted seed string
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA/OAEP decrypt with SHA-256
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Decode bytes to UTF-8 string
    decrypted_seed = decrypted_bytes.decode('utf-8')

    # 4. Validate: must be 64-character hex string
    if len(decrypted_seed) != 64 or not all(c in '0123456789abcdef' for c in decrypted_seed.lower()):
        raise ValueError("Decrypted seed is invalid")

    # 5. Return hex seed
    return decrypted_seed

# -----------------------------
# Run decryption and save to /data/seed.txt
# -----------------------------
# Load private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Read encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed = f.read().strip()

# Decrypt
seed = decrypt_seed(encrypted_seed, private_key)

# Save to /data/seed.txt
os.makedirs("data", exist_ok=True)
with open("data/seed.txt", "w") as f:
    f.write(seed)

print("Decrypted seed saved to data/seed.txt")
