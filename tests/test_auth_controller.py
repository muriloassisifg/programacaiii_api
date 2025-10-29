from fastapi.testclient import TestClient
from main import app
import pytest

# Testes de autenticação e autorização
# Valida login, acesso negado sem token, e token inválido

LOGIN_EMAIL = "murilo.assis@ifg.edu.br"
LOGIN_PASSWORD = "12345678"

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_login_sucesso(client):
    """Testa login com credenciais válidas."""
    response = client.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    assert response.status_code == 200, f"Login falhou: {response.text}"
    assert "access_token" in response.json()


def test_login_invalido(client):
    """Testa login com credenciais inválidas."""
    response = client.post("/auth/login", data={
        "username": "usuario_invalido@ifg.edu.br",
        "password": "senhaerrada"
    })
    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_acesso_sem_token(client):
    """Testa acesso negado a endpoint protegido sem token."""
    response = client.get("/users/")
    assert response.status_code == 401 or response.status_code == 403


def test_acesso_com_token_invalido(client):
    """Testa acesso negado a endpoint protegido com token inválido."""
    headers = {"Authorization": "Bearer token_invalido"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 401 or response.status_code == 403
