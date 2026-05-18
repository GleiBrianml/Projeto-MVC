# Popular o banco de dados com usuários admin

from app.database import Session
from app.models.usuario import Usuario
from app.auth import hash_senha

USUARIOS = [
    {
        "nome": "admin",
        "email": "admin@teste.com",
        "senha": "admin123",
        "role": "admin"
    },
    {
        "nome": "Gleidson",
        "email": "Gleidson@teste.com",
        "senha": "admin123",
        "role": "admin"
    }
]



def criar_usuarios():
    db = Session()
    try:
        for user in USUARIOS:
            existente = db.query(Usuario).filter_by(email=user["email"]).first()
            if existente:
                print(f"Esse email já existe: {user['email']}")
                continue
            else:
                novo_usuario = Usuario(
                    nome=user["nome"],
                    email=user["email"],
                    senha_hash=hash_senha(user["senha"]),
                    role=user["role"]
                )
                db.add(novo_usuario)
                print(f"Usuário criado com sucesso: {user['email']}")
        db.commit()
    except Exception as erro:
        db.rollback()
        print("erro")
    finally:
        db.close()

criar_usuarios()
