from pydantic import BaseModel, Field
from typing import List

class UserIn(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    public_key_pem: str | None = None  # PEM text
    # optional base64-encoded encrypted private key pieces if user wants server to store them:
    priv_salt_b64: str | None = None
    priv_nonce_b64: str | None = None
    priv_cipher_b64: str | None = None

class UserOut(BaseModel):
    id: int
    username: str

class FileMetaOut(BaseModel):
    id: int
    owner_id: int
    orig_filename: str
    created_at: str
    class Config:
        orm_mode = True
