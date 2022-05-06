"""
Citas V2 API OAuth2
"""
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import add_pagination
from sqlalchemy.orm import Session

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from lib.database import get_db

from citas_cliente.v1.autoridades.paths import autoridades
from citas_cliente.v1.cit_clientes.paths import cit_clientes
from citas_cliente.v1.distritos.paths import distritos
from citas_cliente.v1.materias.paths import materias

from citas_cliente.v1.cit_clientes.authentications import authenticate_user, create_access_token, get_current_active_user
from citas_cliente.v1.cit_clientes.schemas import Token, CitClienteInDB

app = FastAPI(
    title="Citas V2 API OAuth2",
    description="API del Sistema de Citas V2 del Poder Judicial del Estado de Coahuila de Zaragoza",
)

app.include_router(autoridades)
app.include_router(cit_clientes)
app.include_router(distritos)
app.include_router(materias)

add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a Citas V2 API OAuth2 del Poder Judicial del Estado de Coahuila de Zaragoza."}


@app.post("/token", response_model=Token)
async def ingresar_para_solicitar_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Entregar el token como un JSON"""
    cit_cliente = authenticate_user(form_data.username, form_data.password, db)
    if not cit_cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": cit_cliente.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", response_model=CitClienteInDB)
async def mi_perfil(current_user: CitClienteInDB = Depends(get_current_active_user)):
    """Mostrar el perfil del cliente"""
    return current_user


@app.post("/recover_account", response_model=Token)
async def recuperar_cuenta():
    """Recuperar cuenta"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@app.post("/new_account", response_model=Token)
async def nueva_cuenta():
    """Nueva cuenta"""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
