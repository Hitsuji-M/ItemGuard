from sqlalchemy.orm import Session

from database.tables import *
from models import *

def create_product(db: Session, model: ProductModel) -> int:
    new_product = Product(idType=model.idType, price=model.price)
    db.add(new_product)
    db.commit()
    return new_product.id