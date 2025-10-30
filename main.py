import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adiciona a pasta app ao Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Importa primeiro a base e engine para evitar problemas de ordem
from database import engine, Base

# Depois importa os controllers
from users import user_controller
from roles import role_controller  
from auth import auth_controller

# Configuração baseada no ambiente
APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

# Criar tabelas apenas em desenvolvimento
if APP_PROFILE == "DEV":
    Base.metadata.create_all(bind=engine)

# 1. Cria a instância principal da aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)

# Configuração de CORS baseada no ambiente
if APP_PROFILE == "DEV":
    # Configuração permissiva para desenvolvimento
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Configuração para produção
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://programacaoiii-front.onrender.com",
            "https://programacaoiii-front.onrender.com/",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# 2. Inclui o roteador de usuários na aplicação principal
app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)

# 4. Código para rodar o servidor
if __name__ == '__main__':
    # Este bloco só executa quando rodamos o script diretamente (python main.py)
    uvicorn.run(app, host="0.0.0.0", port=8000)