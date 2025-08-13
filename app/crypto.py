import os
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

KEYS_DIR = "keys"

# ----------------- Auto Key Generation -----------------
def generate_rsa_key_pair():
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)

    private_key_path = os.path.join(KEYS_DIR, "alice_private.pem")
    public_key_path = os.path.join(KEYS_DIR, "alice_public.pem")

    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        print("[INFO] RSA keys already exist. Skipping generation.")
        return

    print("[INFO] Generating RSA key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    public_key = private_key.public_key()
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"[INFO] Keys generated and saved in '{KEYS_DIR}/'.")

# ----------------- AES Utils -----------------
def generate_aes_key():
    return secrets.token_bytes(32)  # AES-256 key

def aes_encrypt(data: bytes, key: bytes):
    iv = secrets.token_bytes(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ct

def aes_decrypt(enc_data: bytes, key: bytes):
    iv = enc_data[:16]
    ct = enc_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

# ----------------- RSA Utils -----------------
def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def rsa_encrypt(data: bytes, public_key):
    return public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
    )

def rsa_decrypt(enc_data: bytes, private_key):
    return private_key.decrypt(
        enc_data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
    )

# ----------------- Hash -----------------
def sha256_hash(data: bytes):
    return hashlib.sha256(data).hexdigest()

# Generate keys automatically when imported
generate_rsa_key_pair()
