import pytest
from app import app
from src.shared.helpers.auth import auth

@pytest.fixture
def client():
    return app.test_client()

def requester(id_):
    return auth(id_)

def criar_aacd(client, email):
    resposta = client.post("/users", json={"nome": "Teste", "email": email, "senha": "123456"})
    assert resposta.status_code == 201
    return resposta.get_json()["id"]


class Test_DeleteUserPresenter:
    def test_delete_own_user(self, client):
        uid = criar_aacd(client, "del.proprio@aacd.org.br")

        resposta = client.delete(f"/users/{uid}", headers=requester(uid))

        assert resposta.status_code == 200
        assert resposta.get_json()["id"] == uid
        assert "senha_hash" not in resposta.get_json()

        leitura = client.get(f"/users/{uid}", headers=requester(uid))
        assert leitura.status_code == 404

    def test_delete_twice(self, client):
        uid = criar_aacd(client, "del.duas.vezes@aacd.org.br")

        assert client.delete(f"/users/{uid}", headers=requester(uid)).status_code == 200
        assert client.delete(f"/users/{uid}", headers=requester(uid)).status_code == 404

    def test_delete_other_user_is_forbidden(self, client):
        uid = criar_aacd(client, "del.alvo@aacd.org.br")

        resposta = client.delete(f"/users/{uid}", headers=requester(123))

        assert resposta.status_code == 403
        leitura = client.get(f"/users/{uid}", headers=requester(uid))
        assert leitura.status_code == 200

    def test_delete_user_not_found(self, client):
        resposta = client.delete("/users/99999", headers=requester(99999))
        assert resposta.status_code == 404

    def test_delete_without_token(self, client):
        uid = criar_aacd(client, "del.semtoken@aacd.org.br")

        assert client.delete(f"/users/{uid}").status_code == 401
        assert client.get(f"/users/{uid}", headers=requester(uid)).status_code == 200

    def test_old_header_no_longer_works(self, client):
        uid = criar_aacd(client, "del.headerantigo@aacd.org.br")

        resposta = client.delete(f"/users/{uid}", headers={"X-Requester-Id": str(uid)})

        assert resposta.status_code == 401
        assert client.get(f"/users/{uid}", headers=requester(uid)).status_code == 200