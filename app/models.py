from pydantic import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    idProduct: int = None
    idType: int = None
    productName: str = ""
    quantity: int = 0
    price: float = 0.0

class LogModel(BaseModel):
    idType: int
    logDate: datetime = datetime.now()

class UserModel(BaseModel):
    email: str
    passwd: str
    fullName: str = ""
    administrator: bool = False