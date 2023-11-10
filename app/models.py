from pydantic import BaseModel

class ProductModel(BaseModel):
    idType: int
    price: float = 0.0
