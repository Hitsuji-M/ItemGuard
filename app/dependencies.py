from fastapi.security import OAuth2PasswordBearer
from database.setup_db import SessionLocal
from fastapi import Depends, HTTPException, params
from sqlalchemy.orm import Session
from typing import Optional, Callable, Any
from jose import JWTError, jwt

from database.tables import User
from services.auth_services import get_user_by_mail

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, "clubnix", algorithms=["HS256"])
        email: str = payload.get("mail")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_mail(db, email)
    if user is None:
        raise credentials_exception
    
    return user
