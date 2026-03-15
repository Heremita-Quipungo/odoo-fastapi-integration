import os
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from models import Usuario, db
from models import Usuario

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth = OAuth2PasswordBearer(tokenUrl="auth/login-form")

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth), session: Session= Depends(pegar_sessao)):
    try:
        dict_infor = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_infor.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="acesso Negado, verificar a validade do token")   
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario