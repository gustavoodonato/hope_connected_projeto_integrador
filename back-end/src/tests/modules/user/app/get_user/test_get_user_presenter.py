import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def requester(id_):
    return {"X-Requester-Id": str(id_)}


class Test_GetUserPresenter:
    def test_get_own_user(self, client):
        response = client.get("/users/123", headers=requester(123))

        assert response.status_code == 200
        assert response.get_json()["nome"] == "Murilo"
        assert "senha_hash" not in response.get_json()

    def test_get_own_fornecedor_has_endereco(self, client):
        response = client.get("/users/456", headers=requester(456))

        assert response.status_code == 200
        assert response.get_json()["endereco"]["cidade"] == "São Caetano do Sul"

    def test_get_other_user_is_forbidden(self, client):
        response = client.get("/users/456", headers=requester(123))
        assert response.status_code == 403

    def test_get_user_not_found(self, client):
        response = client.get("/users/999", headers=requester(999))
        assert response.status_code == 404

    def test_non_numeric_id(self, client):
        response = client.get("/users/abc", headers=requester(123))
        assert response.status_code == 400

    def test_without_requester_header(self, client):
        response = client.get("/users/123")
        assert response.status_code == 400

    def test_created_user_can_be_retrieved(self, client):
        criado = client.post("/users", json={
            "nome": "Bia", "email": "bia.get.presenter@aacd.org.br", "senha": "123456"})
        assert criado.status_code == 201
        novo_id = criado.get_json()["id"]

        response = client.get(f"/users/{novo_id}", headers=requester(novo_id))

        assert response.status_code == 200
        assert response.get_json()["email"] == "bia.get.presenter@aacd.org.br"