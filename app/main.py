from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controller import auth_controller
from app.controller import admin_controller

from app.auth import get_usuario_opcional

app = FastAPI(title="Sistema MVC")


# CONfigurar o fastAPI para servir os arquivos CSS, JS , IMG
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Cpmfigura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

# Registrar as rotas do controller de autenticação
app.include_router(auth_controller.router)
app.include_router(admin_controller.router)
@app.get("/")
def tela_home(
        request: Request,
        usuario = Depends(get_usuario_opcional)
              
        ):
        # Não logado
        if usuario is None:
            return templates.TemplateResponse(
            request, "index.html",
            {"request": request})
            
        return templates.TemplateResponse(
            request, "home.html",
            {"request": request, "usuario": usuario}
        )