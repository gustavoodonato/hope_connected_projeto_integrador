import pytest
from app import app
from src.shared.helpers.token_handler import TokenHandler

@pytest.fixture
def client():
    return app.test_client()


class Test_LoginPresenter:
    def test_login_mock_user(self, client):
        response = client.post("/login", json={
            "email": "muriloso123@gmail.com", "senha": "senha123"})

        assert response.status_code == 200
        assert TokenHandler.decode(response.get_json()["token"]) == 123

    def test_login_user_created_by_the_api(self, client):

        criado = client.post("/users", json={
            "nome": "Bia", "email": "bia.login.presenter@aacd.org.br", "senha": "minhasenha"})
        assert criado.status_code == 201

        response = client.post("/login", json={
            "email": "bia.login.presenter@aacd.org.br", "senha": "minhasenha"})

        assert response.status_code == 200
        assert response.get_json()["user"]["email"] == "bia.login.presenter@aacd.org.br"

    def test_wrong_password(self, client):
        response = client.post("/login", json={
            "email": "muriloso123@gmail.com", "senha": "errada"})
        assert response.status_code == 401

    def test_without_body(self, client):
        assert client.post("/login").status_code == 400

    def test_get_not_allowed(self, client):
        assert client.get("/login").status_code == 405