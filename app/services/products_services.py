from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from database.tables import *
from models import *
from services.log_services import *

def create_product(db: Session, model: ProductModel) -> int:
    if not model.idType:
        raise HTTPException(status_code=422, detail="Missing values")
    new_product = Product(idtype=model.idType, price=model.price, quantity=model.quantity, productname=model.productName)
    db.add(new_product)
    db.commit()
    add_log(db, LogModel(idType=1))
    return new_product.idproduct

def get_products(db: Session) -> List[Product]:
    return db.query(Product).order_by(Product.idproduct).all()

def get_product_by_id(db: Session, id: int) -> Product:
    record = db.query(Product).filter(Product.idproduct == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Product not found")
    return record

def delete_product_by_id(db: Session, id: int) -> int:
    p = get_product_by_id(db, id)
    db.delete(p)
    db.commit()
    add_log(db, LogModel(idType=3))
    return p.idproduct

def update_product(db: Session, product: ProductModel):
    db_product = get_product_by_id(db, product.idProduct)
    for var, value in vars(product).items():
        setattr(db_product, var.lower(), value) if value else None
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    add_log(db, LogModel(idType=2))
    return db_product

def get_product_types(db: Session) -> List[ProductType]:
    return db.query(ProductType).order_by(ProductType.idtype).all()