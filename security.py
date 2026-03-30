from pwdlib import PasswordHash
from jose import JWTError, jwt
from database import settings
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario

password_hash = PasswordHash.recommended()

oauth_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def criptografar_senha(senha):
    return password_hash.hash(senha)

def verificar_senha(senha, senha_hash):
    return password_hash.verify(senha, senha_hash)

def criar_access_token(dados: dict):
    to_encode = dados.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({'exp': exp})

    access_token = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return access_token

def criar_refresh_token(dados: dict):
    to_encode = dados.copy()
    exp = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expires_days)
    to_encode.update({'exp': exp})

    refresh_token = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return refresh_token

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
    
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail='Usuário não encontrado')
    
    return usuario
