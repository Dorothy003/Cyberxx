from sympy import public
from Aes.aes import encrypt_gcm,decrypt_gcm,generate_aes_key
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64encode

with open("file.txt","r") as f:
    plaintext=f.read().strip()

aes_key=generate_aes_key()
ciphertext=encrypt_gcm(plaintext,aes_key)

with open("Keygen/public_key.pem","rb") as f:
    public_key=serialization.load_pem_public_key(f.read())

encrypted_aes_key=public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("encrypted_key.bin","wb") as f:
    f.write(encrypted_aes_key)

with open("encrypted_message.txt","w") as f:
    f.write(ciphertext)

print("Encryption complete")