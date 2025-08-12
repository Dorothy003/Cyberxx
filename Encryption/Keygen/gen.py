from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def createKey():
    private_key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key=private_key.public_key()

    private_key_pem=private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_pem=public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    private_key_str=private_key_pem.decode('utf-8')
    public_key_str=public_key_pem.decode('utf-8')

    return{
        "publicKey":public_key_str,
        "privateKey":private_key_str
    }


keys=createKey()
with open("public_key.pem","w") as x:
    x.write(keys["publicKey"])
    
with open("private_key.pm","w") as y:
       y.write(keys["privateKey"])
