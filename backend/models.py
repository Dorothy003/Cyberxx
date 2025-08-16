from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    public_key_pem = Column(LargeBinary, nullable=True)  # PEM bytes
    # Optional: encrypted private key stored server-side (salt, nonce, cipher)
    priv_salt = Column(LargeBinary, nullable=True)
    priv_nonce = Column(LargeBinary, nullable=True)
    priv_cipher = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owned_files = relationship("File", back_populates="owner")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    orig_filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    aes_nonce = Column(LargeBinary, nullable=False)
    sha256_hex = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="owned_files")
    recipients = relationship("FileRecipient", back_populates="file", cascade="all, delete-orphan")

class FileRecipient(Base):
    __tablename__ = "file_recipients"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    enc_aes_key = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("File", back_populates="recipients")
    recipient = relationship("User")

    __table_args__ = (UniqueConstraint("file_id", "recipient_id", name="uix_file_recipient"),)

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
