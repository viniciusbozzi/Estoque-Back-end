from pydantic import BaseModel
from enum import Enum

class MovementType(str, Enum):
    entrada = "entrada"
    saida = "saida"

class MovementRequest(BaseModel):
    product_id: int
    type: MovementType
    quantity: int
