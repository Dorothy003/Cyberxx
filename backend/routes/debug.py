from statistics import mode
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models

router=APIRouter()

@router.get("/debug/users")
def debug_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()

# @router.get("/debug/keys")
# def debug_keys(db:Session=Depends(get_db)):
#     return db.query(models.File).all()