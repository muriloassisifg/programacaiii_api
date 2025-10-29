

from fastapi.testclient import TestClient
from main import app
import pytest

# Credenciais para login no sistema
LOGIN_EMAIL = "murilo.assis@ifg.edu.br"
LOGIN_PASSWORD = "12345678"

# Fixture para criar o client e obter o token JWT antes dos testes
@pytest.fixture(scope="module")
def client_and_token():
    client = TestClient(app)
    # Realiza login via API
    login_response = client.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    assert login_response.status_code == 200, f"Login falhou: {login_response.text}"
    token = login_response.json()["access_token"]
    return client, token

def test_user_crud_sequence(client_and_token):
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # Gerar sufixo aleatório para e-mail do usuário de teste
    import random, string
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"test_sequence_user_{random_suffix}@example.com"

    # Buscar uma role existente para vincular ao usuário
    # Garante que sempre haverá uma role válida para o teste
    roles_resp = client.get("/roles/", headers=headers)
    assert roles_resp.status_code == 200 and len(roles_resp.json()) > 0, "Nenhuma role disponível para vincular ao usuário."
    role_id = roles_resp.json()[0]["id"]

    # 1. Criar usuário
    user_data = {
        "email": test_email,
        "password": "password123",
        "full_name": "Test Sequence User",
        "role_id": role_id
    }
    # Chama o endpoint de criação de usuário
    user_resp = client.post("/users/", json=user_data, headers=headers)
    assert user_resp.status_code == 201, f"Falha ao criar usuário: {user_resp.text}"
    user_id = user_resp.json()["id"]
    user_json = user_resp.json()
    assert user_json["email"] == test_email
    assert user_json["full_name"] == "Test Sequence User"
    assert "role" in user_json and user_json["role"]["id"] == role_id

    # 2. Alterar usuário
    update_user_data = {
        "full_name": "Test Sequence User Updated",
        "role_id": role_id
    }
    # Chama o endpoint de atualização de usuário
    update_user_resp = client.put(f"/users/{user_id}", json=update_user_data, headers=headers)
    assert update_user_resp.status_code == 200, f"Falha ao atualizar usuário: {update_user_resp.text}"
    update_json = update_user_resp.json()
    assert update_json["email"] == test_email
    assert update_json["full_name"] == "Test Sequence User Updated"
    assert "role" in update_json and update_json["role"]["id"] == role_id

    # 3. Excluir usuário
    # Chama o endpoint de exclusão de usuário
    delete_user_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_user_resp.status_code == 200, f"Falha ao excluir usuário: {delete_user_resp.text}"
    deleted_json = delete_user_resp.json()
    assert deleted_json["id"] == user_id
    assert deleted_json["email"] == test_email
    assert deleted_json["full_name"] == "Test Sequence User Updated"
    assert "role" in deleted_json and deleted_json["role"]["id"] == role_id