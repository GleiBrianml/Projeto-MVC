from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.controller import auth_controller


app = FastAPI(title="Sistema MVC")

# CONfigurar o fastAPI para servir os arquivos CSS, JS , IMG
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Cpmfigura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

# Registrar as rotas do controller de autenticação
app.include_router(auth_controller.router)
