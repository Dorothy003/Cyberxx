from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os,base64

#from sklearn import base

def encrypt_gcm(plaintext:str,key:bytes)-> str:
    aesgcm=AESGCM(key)
    nonce=os.urandom(12)
    ct=aesgcm.encrypt(nonce,plaintext.encode('utf-8'),associated_data=None)
    return base64.b64encode(nonce+ct).decode('utf-8')

def decrypt_gcm(b64_nonce_ct:str,key:bytes)->str:
    raw=base64.b64decode(b64_nonce_ct)
    nonce,ct=raw[:12],raw[12:]
    aesgcm=AESGCM(key)
    pt=aesgcm.decrypt(nonce,ct,associated_data=None)
    return pt.decode('utf-8')

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)