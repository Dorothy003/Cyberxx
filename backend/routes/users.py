from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.schemas import UserOut

router = APIRouter()

@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.username).all()
    return [{"id": u.id, "username": u.username} for u in users]
