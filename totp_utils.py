import base64
import pyotp

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    
    Args:
        hex_seed: 64-character hex string
    
    Returns:
        6-digit TOTP code as string
    """
    # 1. Convert hex seed to bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # 2. Convert bytes to base32
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')

    # 3. Create TOTP object (SHA-1, 30s period, 6 digits)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # 4. Generate current TOTP code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    
    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: number of periods before/after to accept (default ±1)
    
    Returns:
        True if code is valid, False otherwise
    """
    # Convert hex seed to base32
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')

    # Create TOTP object
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Verify code with ± valid_window periods
    return totp.verify(code, valid_window=valid_window)
