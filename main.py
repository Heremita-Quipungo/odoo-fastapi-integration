from fastapi import FastAPI
from odoo_cliente import create_sale_order, list_sales
from schemas import SaleOrderCreate

app = FastAPI()

from auth_routers import auth_router
from order_routers import order_router

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/sales")
def get_sales():
    return list_sales()


@app.post("/sales")
def create_sale(data: SaleOrderCreate):
    order_id = create_sale_order(
        partner_id=data.partner_id,
        lines=[line.dict() for line in data.lines]
    )
    return {
        "message": "Pedido criado com sucesso",
        "order_id": order_id
    }


# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

