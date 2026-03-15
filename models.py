from sqlalchemy import create_engine,  String, Integer, Boolean, Float, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy_utils import ChoiceType

#Cria a conexão com o seu banco
db=create_engine('sqlite:///database.db')

#Criar banco de dados
Base = declarative_base()

#Criar a classes/tabelas do banco
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome , email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
        self.ativo = ativo


class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedidos", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_pedido(self):
        self.preco = sum(x.preco_unitario * x.quantidade  for x in self.itens)




class ItemPedidos(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("Sabor", Integer)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self,quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

   

# migrar banco de dados

# criar a migraçºao = alembic revision  -- autogenerate -m "alterar repr pedido"
# executar a migração  = alembic upgrade head



