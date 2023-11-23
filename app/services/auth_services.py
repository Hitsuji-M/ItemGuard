from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import hashlib

from database.tables import *
from models import *

def get_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_name(db: Session, username: str):
    user = db.query(User).filter(User.username == username.lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def check_password(db: Session, username: str, password: str) -> bool:
    user = get_user_by_name(db, username)
    return user.psswd == hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()