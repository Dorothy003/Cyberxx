from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, DateTime
from sqlalchemy.sql import func
from .database import Base

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    aes_key_encrypted = Column(LargeBinary, nullable=False)
    recipient = Column(String, nullable=False)
    sender = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    downloaded = Column(Boolean, default=False)
