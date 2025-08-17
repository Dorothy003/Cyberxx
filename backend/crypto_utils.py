import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

BACKEND = default_backend()
RSA_BITS = 3072

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=RSA_BITS, backend=BACKEND)
    public_key = private_key.public_key()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return priv_pem, pub_pem

def aesgcm_encrypt(key: bytes, plaintext: bytes, aad: bytes | None = None):
    if len(key) != 32:
        raise ValueError("AES key must be 32 bytes")
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce, ciphertext

def aesgcm_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes | None = None):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, aad)

def rsa_encrypt(pub_pem: bytes, data: bytes) -> bytes:
    public_key = serialization.load_pem_public_key(pub_pem, backend=BACKEND)
    return public_key.encrypt(
        data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

def rsa_decrypt(priv_pem: bytes, data: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(priv_pem, password=None, backend=BACKEND)
    return private_key.decrypt(
        data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

def sha256_hex(data: bytes) -> str:
    digest = hashes.Hash(hashes.SHA256(), backend=BACKEND)
    digest.update(data)
    return digest.finalize().hex()

# KDF & private key protection (PBKDF2 + AES-GCM)
def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations, backend=BACKEND)
    return kdf.derive(password.encode())

def encrypt_private_key(priv_pem: bytes, password: str):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    nonce, cipher = aesgcm_encrypt(key, priv_pem)
    return salt, nonce, cipher

def decrypt_private_key(salt: bytes, nonce: bytes, cipher: bytes, password: str):
    key = derive_key(password, salt)
    return aesgcm_decrypt(key, nonce, cipher)
