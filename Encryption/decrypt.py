from Aes.aes import decrypt_gcm
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Hardcoded RSA Private Key (replace with your own key)
private_key_pem = b"""-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDNz9hlVRkmzO4J
k79l3Q1lITCg1V+aFBjsH4VSQQZFCSftKooptmaZYDkSr7c9MrWhVYtMy2Su/XO0
JwwNX6x9fNUFkBeBStDdRP/Nw+cOGQY6rxIpT99WT1skRXuINIKMIrPBlSz80stz
BHFZn2Ys2rxeJe1rnIWM2VtAy6tR/tpoO5bkQKV1+akWSpCTqL+IQna7AqCDD0at
6k75IK0mmPokXBLdQg+xl2XKTXODZGZCyJs0rFIOA/BSEKj3+swdo51PL3zB45E6
yxbRQ0q0tEK+korF0UEy6BFQmha0ir202T2s69o1u7XGDBxOHcSzlf1GAeN2jsst
mmiFxn31AgMBAAECggEAEiShyEJkNo4XkzM5ytpdyph5F583ukwjQPgrt0CRiOxx
tJqXa23vmtMSCkUAkPMzcnF+wi+mmeEwnfpYjvqW03PPDkUm4qLxyU/Cgnp5QpOP
f6+HQ6pi3yedD+mAJlWwByKCriy0YTqZQh5rekxu+W1JmxMaMZkEEj08VM304Flq
aT1qFPNplrNCPc7GGq3yIE7isR+LioDfP+eQt3FZnWfCb2gAbqVnd5Bgc4kCgS8k
FoSd74yzHrUezNwN6Nxtkhfsx21Lko7UVI0nqtA7loBvpMmDRDoszwe3tfaod7XB
++kt3IHEqqNS0Mq9vTvBQpcPSsFvkKe9byC5d33UUQKBgQD+1Kk/wzKQn9/91tx2
x1ZpeisL/nX6LBZI2o2poW+chdqgPWrYJh124H4CzXyWEdhDAy5EoGczUxBGH60V
+inif5exKUO/VfbmcVm+e0cTfz3lWuS7JobmR4da2oY2JlVYOWyYVojLMYESBwUL
Q10WPQPmXIRKBBwXbOQ5kLGQmwKBgQDOwZqVLZK5lHt3U7WIv3CM14Oy0MY5igAu
TA8LXHHcKN2NoqeAuk+h/ZgswTJvsO2Q1IQafGcIXVsq9z12S+CUXobco2+ncyTn
IvHHStLAkfud2iUnONags0lBDQtC/5sAJH5Z0NH2Ly6FyWqBtiQQbzr6pleB1wkX
D1ABVj4srwKBgQD3Ec7rAGFlMWzl2s0z6H8Skx1rapKONPKCPkw9XEUvd+QJmqKd
4Q6ONIhYRUz232RTTKEubmrAq1dK9elGNp8neFflr8F8oGda9Clz8mhuMd8cIW1F
OsxuNom4f8jCdZYnjL2KUdQdVejzRpUQX4bASfYfAjJM5QErgSsh2PUf4wKBgQDO
EyfpMmBA+l7JQ7T3lKAwsQoCK5a3ePXPL137W+vcnRqedhVv98MxWVrYmMOVkYpn
xXnaEE59htc8jutCwkQYfdL7jSbXhquseSb1FX3UFGzvG6PWYQ+DYs9LuB2WbL/o
N3d8O+dZ8hLzpBq1KH7vpn3pn+wubM8RneCHRJd53wKBgHu+7e/jgfc54UIuC8zL
eVS11nmyQoUgsVmSwqUnzpxeGB2kUAHb7fFz+VBYG9AVVZqFPpW39HMrdg7uCoNl
cKu0l6HqUswWdH2tzvGGzx9NYR+RIgJ5cq4KvY2NP9+jGzfySPEJbsSLL9IRu+7A
/s03BdRfRkVJSiux6tHQIYEs
-----END PRIVATE KEY-----
"""

# Load private key
private_key = serialization.load_pem_private_key(
    private_key_pem,
    password=None
)

# Read encrypted AES key
with open("encrypted_key.bin", "rb") as f:
    enc = f.read()

# Decrypt AES key
aes_key = private_key.decrypt(
    enc,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Read encrypted message as Base64 text
with open("encrypted_message.txt", "r") as f:
    ciphertext_b64 = f.read().strip()

# Fix Base64 padding if necessary
missing_padding = len(ciphertext_b64) % 4
if missing_padding:
    ciphertext_b64 += "=" * (4 - missing_padding)

# Decrypt message using AES
plaintext = decrypt_gcm(ciphertext_b64, aes_key)

print("Decrypted text:", plaintext)
