from pydantic import BaseModel

class ProductModel(BaseModel):
    idProduct: int = None
    idType: int = None
    price: float = 0.0
