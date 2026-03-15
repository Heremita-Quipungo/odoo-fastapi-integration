import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from security import bcrypt_context, secret_key
from schemas import Usuariochema, LoginSchema






ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, tempo_duracao=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + tempo_duracao

    dict_jwt= {"sub": str(id_usuario), "exp": data_expiracao}

    jwt_codificado = jwt.encode(dict_jwt, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first() 
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario
    

@auth_router.get("/")
async def home():
    return {"message": "Autenticação realizada com sucesso!", "autenticação": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_ch: Usuariochema, session: Session = Depends(pegar_sessao)):
    """Método para criar usuário"""

    usuario = session.query(Usuario).filter(Usuario.email==usuario_ch.email).first() 
    if usuario:
        #return {"message": "Usuário já existe"}
        raise HTTPException(status_code=400, detail=" Email do usuário já cadastrado")
    
    senha_criptografada = bcrypt_context.hash(usuario_ch.senha)
    novo_usuario = Usuario(usuario_ch.nome, usuario_ch.email, senha_criptografada, usuario_ch.activo, usuario_ch.admin)
    session.add(novo_usuario)
    session.commit()

    return {"message": f"Usuário cadastrado com sucesso {usuario_ch.email}"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session= Depends(pegar_sessao)):
    """Endpoint para Fazer o login"""

    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, tempo_duracao=timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session= Depends(pegar_sessao)):
    """Endpoint para Fazer o login"""

    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    access_token = criar_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }  
    

@auth_router.get("/refresh") 
async def use_refresh_token(usuria: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuria.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

 

         



    
    