from pydantic import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    idProduct: int = None
    idType: int = None
    price: float = 0.0

class LogModel(BaseModel):
    idType: int
    logDate: datetime = datetime.now()