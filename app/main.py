from fastapi import FastAPI, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from database.setup_db import engine, SessionLocal, BaseSQL
from models import *

from services import products_services, log_services

app = FastAPI(
    title="ItemGuard",
    description="Inventory software",
    version="0.0.1",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return "ItemGuard on"

@app.get("/db/tables")
def tables():
    return BaseSQL.classes.keys()


###
### /// Logs ///
###


@app.get("/log/view")
def all_logs(db: Session = Depends(get_db)):
    return log_services.all_logs(db)


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