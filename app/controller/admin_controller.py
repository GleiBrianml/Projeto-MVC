from fastapi import APIRouter, Request, Form, status, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario

from app.auth import get_admin, hash_senha

# APIROUTER agrupa as rotas desse arquivo com o prefixo /usuarios
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Configura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")


# ──────────────────────────────────────────────
# LISTAR
# ──────────────────────────────────────────────
@router.get("/")
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_admin),
):
    usuarios = db.query(Usuario).order_by(Usuario.id).all()

    return templates.TemplateResponse(
        request,
        "usuarios/index.html",
        {
            "request": request,
            "admin": admin,
            "usuarios": usuarios,
        },
    )


# ──────────────────────────────────────────────
# CRIAR — exibe o formulário
# ──────────────────────────────────────────────
@router.get("/novo")
def novo_usuario_form(
    request: Request,
    admin=Depends(get_admin),
):
    return templates.TemplateResponse(
        request,
        "usuarios/form.html",
        {
            "request": request,
            "admin": admin,
            "usuario": None,   # sinaliza para o template que é criação
        },
    )


# CRIAR — processa o formulário
@router.post("/novo")
def criar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db),
    admin=Depends(get_admin),
):
    # Verifica e-mail duplicado
    if db.query(Usuario).filter(Usuario.email == email).first():
        return templates.TemplateResponse(
            request,
            "usuarios/form.html",
            {
                "request": request,
                "admin": admin,
                "usuario": None,
                "erro": "Já existe um usuário com esse e-mail.",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    novo = Usuario(
        nome=nome,
        email=email,
        senha=hash_senha(senha),
        role=role,
        ativo=True,
    )
    db.add(novo)
    db.commit()

    return RedirectResponse(
        url="/usuarios/?criado=ok",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# ──────────────────────────────────────────────
# EDITAR — exibe o formulário preenchido
# ──────────────────────────────────────────────
@router.get("/{usuario_id}/editar")
def editar_usuario_form(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_admin),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return templates.TemplateResponse(
        request,
        "usuarios/form.html",
        {
            "request": request,
            "admin": admin,
            "usuario": usuario,  # sinaliza para o template que é edição
        },
    )


# EDITAR — processa o formulário
@router.post("/{usuario_id}/editar")
def atualizar_usuario(
    usuario_id: int,
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    role: str = Form("user"),
    senha: str = Form(""),        # campo opcional: só atualiza se preenchido
    db: Session = Depends(get_db),
    admin=Depends(get_admin),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Verifica e-mail duplicado em outro usuário
    duplicado = (
        db.query(Usuario)
        .filter(Usuario.email == email, Usuario.id != usuario_id)
        .first()
    )
    if duplicado:
        return templates.TemplateResponse(
            request,
            "usuarios/form.html",
            {
                "request": request,
                "admin": admin,
                "usuario": usuario,
                "erro": "Já existe outro usuário com esse e-mail.",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    usuario.nome = nome
    usuario.email = email
    usuario.role = role

    if senha.strip():                      # só troca a senha se o campo vier preenchido
        usuario.senha = hash_senha(senha)

    db.commit()

    return RedirectResponse(
        url="/usuarios/?editado=ok",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# ──────────────────────────────────────────────
# TOGGLE ATIVO / INATIVO
# ──────────────────────────────────────────────
@router.post("/{usuario_id}/toggle-ativo")
def toggle_ativo(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_admin),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Admin não pode desativar a própria conta
    if usuario.id == admin.get("id"):
        return RedirectResponse(
            url="/usuarios/?erro=autoproprio",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    usuario.ativo = not usuario.ativo
    db.commit()

    return RedirectResponse(
        url="/usuarios/",
        status_code=status.HTTP_303_SEE_OTHER,
    )