from fastapi import FastAPI, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware import cors
from sqlalchemy.orm import Session
from starlette.middleware import sessions
from datetime import datetime as dt

from database.setup_db import BaseSQL
from models import *
from database.tables import User
from dependencies import (
    get_db,
    get_current_user,
    redirect_after_login,
    check_admin
) 

import services.auth_services as auth_services
import services.log_services as log_services
import services.products_services as products_services

REDIRECT = False

app = FastAPI(
    title="ItemGuard",
    description="Inventory software",
    version="0.0.1",
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(sessions.SessionMiddleware, secret_key="clubnix")


@app.get("/")
def root():
    return "ItemGuard on"

@app.get("/db/tables")
def tables():
    return BaseSQL.classes.keys()


###
### /// Authentication ///
###


@app.post("/login")
def final_auth(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login route. Takes a Request Form as a parameter wit the values :
    - grant_type = 'password'
    - username = your_username
    - password = your_password

    Set the cookie "token" in the response then returns the authorization token or redirect to another page
    """
    model = UserModel(email=form_data.username, passwd=form_data.password)
    token_infos = auth_services.login(db, model)
    response.set_cookie(key="token", value=token_infos["access_token"])
    if REDIRECT:
        return redirect_after_login(db, token_infos["access_token"])
    return token_infos


@app.post("/register")
def register_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    The register route creates a user in the database then calls the login service as the login route
    """
    model = UserModel(email=form_data.username, passwd=form_data.password)
    auth_services.register(db, model)
    token_infos = auth_services.login(db, model)
    if REDIRECT:
        return redirect_after_login(db, token_infos["access_token"])
    return token_infos


@app.put("/user/update")
def update_user_profile(updated_profile: UserModel, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if updated_profile.administrator != user.administrator:
        check_admin(user)
    return auth_services.update_user_profile(db, user.email, updated_profile)
        

###
### /// User ///
###


@app.get("/user/accueil")
def user_main(user: User = Depends(get_current_user)):
    return {"user": user.email}

@app.get("/user/me")
def user_profile(user: User = Depends(get_current_user)):
    return user


###
### /// Administrator ///
###

@app.get("/admin/accueil")
async def admin_main(user: User = Depends(get_current_user)):
    check_admin(user)
    return {"user": user.email}

@app.get("/admin/me")
async def admin_profile(user: User = Depends(get_current_user)):
    check_admin(user)
    return user

###
### /// Logs ///
###


@app.get("/logs")
def all_logs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return log_services.get_logs(db)

@app.get("/logs/search")
def search(limit: int = 0, desc: bool = True, before: dt = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return log_services.logs_query(db, limit=limit, desc=desc, before=before)

@app.get("/logs/{limit}")
def all_logs_limit(limit: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return log_services.get_logs_limited(db, limit)

@app.delete("/log/{id}")
def rm_log(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return log_services.delete_log_by_id(db, id)


###
### /// Products ///
###


@app.post("/product")
def new_product(product: ProductModel, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return products_services.create_product(db, product)

@app.get("/products")
def all_products(db: Session = Depends(get_db)):
    return products_services.get_products(db)

@app.get("/product/{id}")
def single_product(id: int, db: Session = Depends(get_db)):
    return products_services.get_product_by_id(db, id)

@app.delete("/product/{id}")
def remove_product(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return products_services.delete_product_by_id(db, id)

@app.put("/product")
def upd_product(product: ProductModel, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    check_admin(user)
    return products_services.update_product(db, product)

@app.get("/types/product")
def all_product_types(db: Session = Depends(get_db)):
    return products_services.get_product_types(db)