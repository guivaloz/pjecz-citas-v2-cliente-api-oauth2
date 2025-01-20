"""
PJECZ Citas cliente API OAuth2
"""

from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import add_pagination
from sqlalchemy.orm import Session

from .cruds.v2.authentications import authenticate_user, create_access_token, get_current_active_user
from .dependencies.database import get_db
from .routers.v2.autoridades import autoridades as autoridades_v2
from .routers.v2.cit_citas import cit_citas_v2
from .routers.v2.cit_clientes import cit_clientes_v2
from .routers.v2.cit_clientes_recuperaciones import cit_clientes_recuperaciones_v2
from .routers.v2.cit_clientes_registros import cit_clientes_registros_v2
from .routers.v2.cit_dias_disponibles import cit_dias_disponibles_v2
from .routers.v2.cit_horas_disponibles import cit_horas_disponibles_v2
from .routers.v2.cit_oficinas_servicios import cit_oficinas_servicios_v2
from .routers.v2.cit_servicios import cit_servicios_v2
from .routers.v2.distritos import distritos as distritos_v2
from .routers.v2.domicilios import domicilios_v2
from .routers.v2.enc_servicios import enc_servicios_v2
from .routers.v2.enc_sistemas import enc_sistemas_v2
from .routers.v2.materias import materias_v2
from .routers.v2.oficinas import oficinas_v2
from .routers.v3.autoridades import autoridades as autoridades_v3
from .routers.v3.distritos import distritos as distritos_v3
from .routers.v3.municipios import municipios as municipios_v3
from .routers.v3.pag_pagos import pag_pagos as pag_pagos_v3
from .routers.v3.pag_tramites_servicios import pag_tramites_servicios as pag_tramites_servicios_v3
from .routers.v3.ppa_solicitudes import ppa_solicitudes as ppa_solicitudes_v3
from .routers.v3.tdt_partidos import tdt_partidos as tdt_partidos_v3
from .routers.v3.tdt_solicitudes import tdt_solicitudes as tdt_solicitudes_v3
from .schemas.v2.cit_clientes import CitClienteInDB, Token
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, ORIGINS

# FastAPI
app = FastAPI(
    title="PJECZ Citas Cliente API OAuth2",
    description="API del sistema de citas para la interfaz del cliente.",
    docs_url="/docs",
    redoc_url=None,
)

# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(autoridades_v2)
app.include_router(distritos_v2)
app.include_router(cit_citas_v2)
app.include_router(cit_clientes_v2)
app.include_router(cit_clientes_recuperaciones_v2)
app.include_router(cit_clientes_registros_v2)
app.include_router(cit_dias_disponibles_v2)
app.include_router(cit_horas_disponibles_v2)
app.include_router(cit_oficinas_servicios_v2)
app.include_router(cit_servicios_v2)
app.include_router(domicilios_v2)
app.include_router(enc_servicios_v2)
app.include_router(enc_sistemas_v2)
app.include_router(materias_v2)
app.include_router(oficinas_v2)

app.include_router(autoridades_v3)
app.include_router(distritos_v3)
app.include_router(municipios_v3)
app.include_router(pag_pagos_v3)
app.include_router(pag_tramites_servicios_v3)
app.include_router(ppa_solicitudes_v3)
app.include_router(tdt_partidos_v3)
app.include_router(tdt_solicitudes_v3)

# Pagination
add_pagination(app)


@app.get("/")
async def root():
    """Mensaje de Bienvenida"""
    return {"message": "Bienvenido a PJECZ Citas Cliente API OAuth2."}


@app.post("/token", response_model=Token)
@app.post("/v2/token", response_model=Token)
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
    return {"access_token": access_token, "token_type": "bearer", "username": cit_cliente.username}


@app.get("/profile", response_model=CitClienteInDB)
@app.get("/v2/profile", response_model=CitClienteInDB)
async def mi_perfil(current_user: CitClienteInDB = Depends(get_current_active_user)):
    """Mostrar el perfil del cliente"""
    return current_user
