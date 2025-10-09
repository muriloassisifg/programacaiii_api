# main.py - Entry point for deployment
import sys
import os

# Adiciona a pasta app ao Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Importa a aplicação da pasta app
from main import app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)