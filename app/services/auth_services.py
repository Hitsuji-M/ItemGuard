from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from jose import jwt
from datetime import datetime as dt
from datetime import timedelta

import hashlib

from database.tables import *
from models import *

def hash_password(password: str) -> str:
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    return hashed == hash_password(password)


#
#
#


def get_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_mail(db: Session, email: str):
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_auth(db: Session, model: UserModel):
    try:
        user = get_user_by_mail(db, model.email)
    except HTTPException as e:
        user = None

    if user and check_password(model.passwd, user.passwd):
        return user

def register(db: Session, model: UserModel) -> int:
    if get_user_by_mail(db, model.email):
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = hash_password(model.passwd)
    new_user = User(email=model.email, passwd=hashed_password, fullName=model.fullName, administrator=False)
    db.add()
    db.commit()
    db.refresh()
    return new_user.iduser

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expiration = dt.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(claims=to_encode, key="clubnix", algorithm="HS256")
    return encoded_jwt