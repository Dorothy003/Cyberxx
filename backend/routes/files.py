
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os, io, uuid
from backend.database import get_db
from backend.models import User, File, FileRecipient, Activity
from backend.crypto_utils import aesgcm_encrypt, aesgcm_decrypt, rsa_encrypt, rsa_decrypt, sha256_hex, decrypt_private_key
import base64

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def get_user_or_404(db: Session, username: str) -> User:
    u = db.query(User).filter(User.username == username).first()
    if not u:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return u

@router.post("/upload")
async def upload_file(
    owner: str=Form(...),
    recipients: List[str] = Form(...),
    f: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
):
    owner_user = get_user_or_404(db, owner)

    data = await f.read()
    file_hash = sha256_hex(data)

    aes_key = os.urandom(32)
    nonce, ciphertext = aesgcm_encrypt(aes_key, data)

    stored_name = f"{uuid.uuid4().hex}"
    stored_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(stored_path, "wb") as out:
        out.write(ciphertext)

    file_rec = File(
        owner_id=owner_user.id,
        orig_filename=f.filename,
        stored_path=stored_path,
        aes_nonce=nonce,
        sha256_hex=file_hash,
    )
    db.add(file_rec)
    db.commit()
    db.refresh(file_rec)

    # for each recipient, wrap AES key with their public key
    for rname in recipients:
        recipient_user = get_user_or_404(db, rname)
        if not recipient_user.public_key_pem:
            # skip or raise error
            raise HTTPException(status_code=400, detail=f"Recipient {rname} has no public key")
        enc_key = rsa_encrypt(recipient_user.public_key_pem, aes_key)
        fr = FileRecipient(file_id=file_rec.id, recipient_id=recipient_user.id, enc_aes_key=enc_key)
        db.add(fr)
    db.add(Activity(username=owner_user.username, text=f"uploaded {f.filename}"))
    db.commit()
    return {"id": file_rec.id, "orig_filename": file_rec.orig_filename, "owner_id": file_rec.owner_id}

@router.get("")
def list_files(username: str, db: Session = Depends(get_db)):
    user = get_user_or_404(db, username)
    q = (
        db.query(File, User.username)
        .join(FileRecipient, FileRecipient.file_id == File.id)
        .join(User, User.id == File.owner_id)
        .filter(FileRecipient.recipient_id == user.id)
        .order_by(File.created_at.desc())
    )
    out = [{"id": f.id, "orig_filename": f.orig_filename, "owner": u} for (f, u) in q.all()]
    return out

@router.get("/{file_id}/download")
def download_file(file_id: int, username: str, db: Session = Depends(get_db)):
    user = get_user_or_404(db, username)
    file_rec = db.query(File).filter(File.id == file_id).first()
    if not file_rec:
        raise HTTPException(status_code=404, detail="File not found")

    fr = db.query(FileRecipient).filter(
        FileRecipient.file_id == file_id, FileRecipient.recipient_id == user.id
    ).first()
    if not fr:
        raise HTTPException(status_code=403, detail="You do not have access to this file")

    # Use server-side stored encrypted private key
    if not (user.priv_salt and user.priv_nonce and user.priv_cipher):
        raise HTTPException(status_code=400, detail="Private key not stored on server")

    try:
        # Decrypt private key without password (server-side)
        priv_pem = decrypt_private_key(user.priv_salt, user.priv_nonce, user.priv_cipher)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decrypt private key")

    try:
        # RSA unwrap AES key
        aes_key = rsa_decrypt(priv_pem, fr.enc_aes_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decrypt AES key with private key")

    # Decrypt the file
    if not os.path.exists(file_rec.stored_path):
        raise HTTPException(status_code=500, detail="Encrypted file missing on server")
    with open(file_rec.stored_path, "rb") as fh:
        ciphertext = fh.read()
    try:
        plaintext = aesgcm_decrypt(aes_key, file_rec.aes_nonce, ciphertext)
    except Exception:
        raise HTTPException(status_code=500, detail="AES decryption failed or tag invalid")

    # Verify hash
    if sha256_hex(plaintext) != file_rec.sha256_hex:
        raise HTTPException(status_code=500, detail="Integrity check failed (SHA-256 mismatch)")

    # Record activity
    db.add(Activity(username=user.username, text=f"downloaded {file_rec.orig_filename}"))
    db.commit()

    # Stream file
    return StreamingResponse(
        io.BytesIO(plaintext),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_rec.orig_filename}"'}
    )

