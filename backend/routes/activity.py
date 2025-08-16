from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Activity
from typing import List

router = APIRouter()

@router.get("", response_model=List[dict])
def get_activity(username: str | None = None, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Activity)
    if username:
        q = q.filter(Activity.username == username)
    q = q.order_by(Activity.created_at.desc()).limit(limit)
    return [{"username": a.username, "text": a.text, "created_at": a.created_at.isoformat()} for a in q.all()]
