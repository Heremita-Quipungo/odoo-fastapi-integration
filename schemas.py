from pydantic import BaseModel
from typing import Optional, List


class Usuariochema(BaseModel):
    nome:  str
    email: str
    senha:str
    activo: Optional[bool]
    admin :Optional[bool]
    
    class config:
        from_attributes = True

class PedidosSchemas(BaseModel):
    id_usuario: int

    class config:
        from_attributes = True

class LoginSchema(BaseModel):
    senha: str
    email: str
    class config:
        from_attributes = True

class ItemPeidosSchema(BaseModel): 
        quantidade: int 
        sabor: str
        tamanho: str
        preco_unitario: float
        class config:
            from_attributes = True


class ResponsePeidosSchema(BaseModel): 
        id: int 
        status: str
        preco: float

        class config:
            from_attributes = True  

#integração odoo  
class SaleOrderLine(BaseModel):
    product_id: int
    qty: float
    price: float


class SaleOrderCreate(BaseModel):
    partner_id: int
    lines: List[SaleOrderLine]                     
          