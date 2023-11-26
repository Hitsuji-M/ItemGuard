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

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expiration = dt.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(claims=to_encode, key="clubnix", algorithm="HS256")
    return encoded_jwt

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
    except HTTPException as _:
        user = None

    if user and check_password(model.passwd, user.passwd):
        return user

def register(db: Session, model: UserModel) -> int:
    user = None
    try:
        user = get_user_by_mail(db, model.email)
    except HTTPException as _:
        pass

    if user:
        raise HTTPException(status_code=409, detail="User already exists")

    hashed_password = hash_password(model.passwd)
    new_user = User(email=model.email, passwd=hashed_password, fullname=model.fullName, administrator=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.iduser

def login(db: Session, model: UserModel) -> dict:
    user = get_user_by_auth(db, model)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_token(data={"mail": user.email})
    return {"access_token": token, "token_type": "bearer"}