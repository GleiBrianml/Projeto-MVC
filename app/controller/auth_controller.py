from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

# APIROUTER para renderizar os templates HTML
router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Configura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

# Rota para tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request, "auth/cadastro.html",
        {"request": request})
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request, "auth/login.html",
        {"request": request})