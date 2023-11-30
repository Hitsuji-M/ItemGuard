from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from database.setup_db import SessionLocal
from sqlalchemy.orm import Session

from database.tables import User
from services.auth_services import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

def get_db():
    print("Hello3")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session(request: Request):
    return request


def get_current_user(
    request: Request = Depends(get_session),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    if "token" in request.cookies:
        token = request.cookies["token"]

    return get_user_by_token(db, token)


def redirect_after_login(db: Session, token: str) -> RedirectResponse:
    user = get_user_by_token(db, token)
    if user.administrator:
        response = RedirectResponse(url="/admin/accueil", status_code=303, headers={"Authorization": "Bearer " + token})
        response.set_cookie(key="token", value=token)
    else:
        response = RedirectResponse(url="/user/accueil", status_code=303, headers={"Authorization": "Bearer " + token})
        response.set_cookie(key="token", value=token)
    return response


def check_admin(user: User) -> None:
    if not user.administrator:
        raise HTTPException(status_code=401, detail="Unhautorized")