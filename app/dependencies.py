from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from database.setup_db import SessionLocal
from sqlalchemy.orm import Session

from database.tables import User
from services.auth_services import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

def get_db():
    """
    Returns the database session to perform queries
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session(request: Request):
    "Returns the current session used by the user"
    return request


def get_current_user(
    request: Request = Depends(get_session),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current user based on his authorization
    Check if 'token' cookie exists or get the token from the 'Authorization' header

    returns the corresponding user
    """

    if "token" in request.cookies:
        token = request.cookies["token"]

    return get_user_by_token(db, token)


def redirect_after_login(db: Session, token: str) -> RedirectResponse:
    """
    Redirect the user after a login based on his administrator access
    """

    user = get_user_by_token(db, token)
    if user.administrator:
        response = RedirectResponse(url="/admin/accueil", status_code=303, headers={"Authorization": "Bearer " + token})
        response.set_cookie(key="token", value=token)
    else:
        response = RedirectResponse(url="/user/accueil", status_code=303, headers={"Authorization": "Bearer " + token})
        response.set_cookie(key="token", value=token)
    return response


def check_admin(user: User) -> None:
    """Check if the user has admin privilege. If not raise a 401 error"""
    if not user.administrator:
        raise HTTPException(status_code=401, detail="Unhautorized")