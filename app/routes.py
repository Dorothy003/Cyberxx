from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import Transfer
from .crypto import generate_aes_key, aes_encrypt, rsa_encrypt, sha256_hash, load_public_key, aes_decrypt, rsa_decrypt, load_private_key
import os
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

UPLOAD_DIR = "uploads/"
KEYS_DIR = "keys/"

@router.post("/upload")
async def upload_file(recipient: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    contents = await file.read()
    aes_key = generate_aes_key()
    encrypted_file = aes_encrypt(contents, aes_key)

    public_key_path = os.path.join(KEYS_DIR, f"{recipient}_public.pem")
    if not os.path.exists(public_key_path):
        raise HTTPException(404, "Recipient public key not found")
    public_key = load_public_key(public_key_path)

    encrypted_aes_key = rsa_encrypt(aes_key, public_key)
    file_hash = sha256_hash(contents)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    stored_filename = f"{file.filename}_{int(os.times().elapsed * 1000)}.enc"
    stored_path = os.path.join(UPLOAD_DIR, stored_filename)
    with open(stored_path, "wb") as f:
        f.write(encrypted_file)

    new_transfer = Transfer(
        filename=file.filename,
        stored_path=stored_path,
        file_hash=file_hash,
        aes_key_encrypted=encrypted_aes_key,
        recipient=recipient,
        sender=None,
    )
    db.add(new_transfer)
    await db.commit()
    await db.refresh(new_transfer)

    return {"transfer_id": new_transfer.id, "filename": new_transfer.filename}

@router.get("/download/{transfer_id}")
async def download_file(transfer_id: int, recipient: str):
    from .database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        transfer = await db.get(Transfer, transfer_id)
        if not transfer:
            raise HTTPException(404, "Transfer not found")
        if transfer.recipient != recipient:
            raise HTTPException(403, "You are not the recipient")

        private_key_path = os.path.join(KEYS_DIR, f"{recipient}_private.pem")
        if not os.path.exists(private_key_path):
            raise HTTPException(404, "Recipient private key not found")
        private_key = load_private_key(private_key_path)

        aes_key = rsa_decrypt(transfer.aes_key_encrypted, private_key)

        with open(transfer.stored_path, "rb") as f:
            encrypted_file = f.read()

        decrypted_file = aes_decrypt(encrypted_file, aes_key)

        if sha256_hash(decrypted_file) != transfer.file_hash:
            raise HTTPException(400, "File integrity check failed")

        return StreamingResponse(io.BytesIO(decrypted_file), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={transfer.filename}"})
