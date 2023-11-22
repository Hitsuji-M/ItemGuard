from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime as dt

from database.setup_db import SessionLocal, BaseSQL
from models import *
from services import log_services, products_services

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