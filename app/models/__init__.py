from app.models import categoria
from app.models import produto
from app.models import usuario


# Gerar a migration
# python -m alembic revision --autogenerate -m "Criar tabelas categoria, produto e usuario"

# python -m alembic upgrade head