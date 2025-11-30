from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Step 2: Generate Student Key Pair
def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair

    Returns:
        Tuple of (private_key_pem_bytes, public_key_pem_bytes) objects

    Implementation:
    - Use your language's crypto library to generate 4096-bit RSA key
    - Set public exponent to 65537
    - Serialize to PEM format
    - Return key objects for further use
    """

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    # Convert private key to PEM (unencrypted PKCS#8)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Extract public key
    public_key = private_key.public_key()

    # Convert public key to PEM (SubjectPublicKeyInfo)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


if __name__ == "__main__":
    # Generate keys
    private_pem, public_pem = generate_rsa_keypair()

    # Save to files as required by assignment
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)

    with open("student_public.pem", "wb") as f:
        f.write(public_pem)

    print("Student RSA 4096-bit key pair generated successfully!")
