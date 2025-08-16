from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.crypto_utils import generate_rsa_keypair, sha256_hex
import base64
from pathlib import Path

router = APIRouter()

KEYS_DIR = Path("keys")
KEYS_DIR.mkdir(exist_ok=True)

@router.post("/generate")
def generate_keys():
    priv, pub = generate_rsa_keypair()
    # return PEM decoded as utf-8 strings (clients can store private locally)
    return {"private_key": priv.decode(), "public_key": pub.decode()}

@router.post("/upload")
def upload_keys(payload: dict, db: Session = Depends(get_db)):
    """
    Accepts JSON:
    { "username": "...", "public_key_pem": "...", optional priv_salt_b64, priv_nonce_b64, priv_cipher_b64 }
    """
    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="username required")
    user = db.query(User).filter(User.username == username).first()
    pub_text = payload.get("public_key_pem")
    if user is None:
        user = User(username=username)
    if pub_text:
        user.public_key_pem = pub_text.encode()
    # store optional encrypted private key pieces (base64 strings)
    if payload.get("priv_salt_b64"):
        user.priv_salt = base64.b64decode(payload["priv_salt_b64"])
    if payload.get("priv_nonce_b64"):
        user.priv_nonce = base64.b64decode(payload["priv_nonce_b64"])
    if payload.get("priv_cipher_b64"):
        user.priv_cipher = base64.b64decode(payload["priv_cipher_b64"])
   
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@router.get("/status")
def key_status(username: str | None = None, db: Session = Depends(get_db)):
    if username:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return JSONResponse(None, status_code=200)
        if user.public_key_pem:
            fingerprint = sha256_hex(user.public_key_pem)[:16]
            return {"status": "active", "fingerprint": fingerprint}
        return JSONResponse(None, status_code=200)
    # no username: return basic presence info
    users = db.query(User).all()
    return [{"username": u.username, "has_public": bool(u.public_key_pem)} for u in users]

@router.get("/public")
def download_public(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.public_key_pem:
        raise HTTPException(status_code=404, detail="Public key not found")
    # return as text/plain
    return JSONResponse({"public_key": user.public_key_pem.decode()})
