from fastapi import FastAPI, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware import cors
from sqlalchemy.orm import Session
from starlette.middleware import sessions
from datetime import datetime as dt

from database.setup_db import BaseSQL
from models import *
from database.tables import User
from dependencies import get_db, get_current_user

import services.auth_services as auth_services
import services.log_services as log_services
import services.products_services as products_services


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


@app.post("/auth")
def final_auth(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    model = UserModel(email=form_data.username, passwd=form_data.password)
    token_infos = auth_services.login(db, model)
    response.set_cookie("token", token_infos["access_token"])
    return token_infos

#Filer les deux trucs en body
@app.post("/user/register")
def register_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    model = UserModel(email=form_data.username, passwd=form_data.password)
    auth_services.register(db, model)
    return auth_services.login(db, model)

@app.get("/user/me")
async def profile(user: User = Depends(get_current_user)):
    if user is None:
        return RedirectResponse(url="/user/login")
    return user


###
### /// Logs ///
###


@app.get("/logs")
def all_logs(db: Session = Depends(get_db)):
    return log_services.get_logs(db)

@app.get("/logs/search")
def search(limit: int = 0, desc: bool = True, before: dt = None, db: Session = Depends(get_db)):
    return log_services.logs_query(db, limit=limit, desc=desc, before=before)

@app.get("/logs/{limit}")
def all_logs_limit(limit: int, db: Session = Depends(get_db)):
    return log_services.get_logs_limited(db, limit)

@app.delete("/log/{id}")
def rm_log(id: int, db: Session = Depends(get_db)):
    return log_services.delete_log_by_id(db, id)


###
### /// Products ///
###


@app.post("/product")
def create_product(product: ProductModel, db: Session = Depends(get_db)):
    return products_services.create_product(db, product)

@app.get("/products")
def all_products(db: Session = Depends(get_db)):
    return products_services.get_products(db)

@app.delete("/product/{id}")
def rm_product(id: int, db: Session = Depends(get_db)):
    return products_services.delete_product_by_id(db, id)

@app.put("/product")
def upd_product(product: ProductModel, db: Session = Depends(get_db)):
    return products_services.update_product(db, product)