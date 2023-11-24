from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime as dt

from database.setup_db import BaseSQL
from models import *
from database.tables import User
from services import log_services, products_services, auth_services
from dependencies import get_db, get_current_user

app = FastAPI(
    title="ItemGuard",
    description="Inventory software",
    version="0.0.1",
)


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
def final_auth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    model = UserModel(email=form_data.username, passwd=form_data.password)
    user = auth_services.get_user_by_auth(db, model)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_services.create_token(data={"mail": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/user/register")
async def register_user(model: UserModel, db: Session = Depends(get_db)):
    return auth_services.register(db, model)

@app.post("/user/login")
async def login_user(db: Session = Depends(get_db)):
    pass


@app.get("/user/me")
async def profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        return RedirectResponse(url="/login")
    return User


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