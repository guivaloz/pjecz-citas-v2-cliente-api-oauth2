"""
Autentificaciones
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.settings import SECRET_KEY, ALGORITHM
from lib.database import get_db

from ...core.cit_clientes.models import CitCliente
from .schemas import TokenData, CitClienteInDB

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")  # In tutorial use schemes=["bcrypt"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """Validar contraseña"""
    # Maybe the hashed_password is not a string or is an empty string
    if not isinstance(hashed_password, str) or hashed_password == "":
        return False
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Cifrar contraseña"""
    return pwd_context.hash(password)


def get_cit_cliente(username: str, db: Session = Depends(get_db)):
    """Obtener el cliente a partir de su e-mail"""
    cit_cliente = db.query(CitCliente).filter(CitCliente.email == username).first()
    if cit_cliente:
        datos = {
            "id": cit_cliente.id,
            "nombres": cit_cliente.nombres,
            "apellido_primero": cit_cliente.apellido_primero,
            "apellido_segundo": cit_cliente.apellido_segundo,
            "curp": cit_cliente.curp,
            "telefono": cit_cliente.telefono,
            "email": cit_cliente.email,
            "limite_citas_pendientes": cit_cliente.limite_citas_pendientes,
            "autoriza_mensajes": cit_cliente.autoriza_mensajes,
            "enviar_boletin": cit_cliente.enviar_boletin,
            "username": cit_cliente.email,
            "permissions": cit_cliente.permissions,
            "hashed_password": cit_cliente.contrasena_sha256,
            "disabled": cit_cliente.estatus != "A",
        }
        return CitClienteInDB(**datos)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """Autentificar el cliente"""
    cit_cliente = get_cit_cliente(username, db)
    print(repr(cit_cliente))
    if not cit_cliente:
        return False
    if not verify_password(password, cit_cliente.hashed_password):
        return False
    return cit_cliente


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear el token de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Obtener el usuario a partir del token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    usuario = get_cit_cliente(token_data.username, db)
    if usuario is None:
        raise credentials_exception
    return usuario


async def get_current_active_user(current_user: CitClienteInDB = Depends(get_current_user)):
    """Obtener el usuario a partir del token y provocar error si está inactivo"""
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized (usuario inactivo)")
    return current_user
