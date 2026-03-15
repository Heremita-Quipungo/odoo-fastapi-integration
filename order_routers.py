from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidosSchemas, ItemPeidosSchema, ResponsePeidosSchema
from models import Pedido, Usuario, ItemPedidos
from dotenv import load_dotenv
from dependencies import verificar_token
from typing import List


order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])


@order_router.post("/pedido")
async def criar_pedidos(pedidos_schemas: PedidosSchemas, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedidos_schemas.id_usuario)
    session.add(novo_pedido) 
    session.commit()
    return {"mensagen": f"Pedido criado com sucesso: {novo_pedido.id}"}

@order_router.post("/pedidos/cancelar/{id_pedido}")
async def cancelar_pedidos(id_pedido: int, session: Session=Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    print(f" o usuario {usuario.id}   e o pedido {pedido.usuario}")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para apgar este pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagen": f"Pedido número: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session=Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permisão para fazer esta operação")
    else :
        pedidos = session.query(Pedido).all()
    return  {
        "pedidos": pedidos
    }  

@order_router.post("/pedidos/adicionar-item/{id_pedido}")
async def adicionar_pedido(id_pedido: int, item_pedido_schema: ItemPeidosSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="tu não tens permissão para efectuar esta operação")
    item_pedido = ItemPedidos(item_pedido_schema.quantidade, item_pedido_schema.sabor, 
                              item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)
    
    session.add(item_pedido)
    pedido.calcular_pedido()
    session.commit()
    return {
        "mensagem": "item criado com sucesso",
        "item_id": item_pedido.id,
        "preco do pedido": pedido.preco
    }


@order_router.post("/pedidos/remover-item/{item_pedido}")
async def remover_pedido(item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    var_item_pedido = session.query(ItemPedidos).filter(ItemPedidos.id==item_pedido).first()
    if not var_item_pedido:
        raise HTTPException(status_code=400, detail="Item não encontrado não encontrado")
    pedido = session.query(Pedido).filter(Pedido.id==var_item_pedido.pedido).first()
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="tu não tens permissão para efectuar esta operação")
    session.delete(var_item_pedido)
    pedido.calcular_pedido()
    session.commit()
    return {
    "mensagem": "item removido com sucesso",
    "preco_do_pedido": pedido.preco,
    "pedido_id": pedido.id
}


@order_router.post("/pedidos/finalizar/{id_pedido}")
async def finalizar_pedidos(id_pedido: int, session: Session=Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para apgar este pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagen": f"Pedido número: {pedido.id} Finalizado com sucesso",
        "pedido": pedido
    }


@order_router.get("/visualizar-pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int ,session: Session=Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permisão para fazer esta operação")
    return  {
        "QUantidade de pedido": len(pedido.itens),
        "DAdos do pedido": pedido
    } 


@order_router.get("/listar/pedidos-usuario/", response_model= List[ResponsePeidosSchema])
async def listar_propios_pedidos(session: Session=Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    if not pedidos:
        raise HTTPException(status_code=400, detail="Nenhum pedido encontrado")
    return  pedidos




    