import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


class Test_CreateUserPresenter:
    def test_post_aacd(self, client):
        response = client.post("/users", json={
            "nome": "Ana", "email": "ana.presenter@aacd.org.br", "senha": "123456"})

        assert response.status_code == 201
        assert response.get_json()["email"] == "ana.presenter@aacd.org.br"
        assert "senha_hash" not in response.get_json()

    def test_post_fornecedor(self, client):
        response = client.post("/users", json={
            "nome": "IBM", "email": "ibm.presenter@gmail.com", "senha": "654321",
            "phone": "88999994444",
            "endereco": {"cep": "01023330", "logradouro": "Rua A", "numero": "1",
                         "bairro": "Centro", "cidade": "São Paulo", "estado": "SP"}})

        assert response.status_code == 201
        assert response.get_json()["endereco"]["cidade"] == "São Paulo"

    def test_post_duplicated_email(self, client):
        corpo = {"nome": "Bia", "email": "bia.presenter@aacd.org.br", "senha": "123456"}

        assert client.post("/users", json=corpo).status_code == 201
        assert client.post("/users", json=corpo).status_code == 409

    def test_post_without_body(self, client):
        assert client.post("/users").status_code == 400

    def test_other_methods_not_allowed(self, client):
        assert client.delete("/users").status_code == 405
        assert client.put("/users").status_code == 405