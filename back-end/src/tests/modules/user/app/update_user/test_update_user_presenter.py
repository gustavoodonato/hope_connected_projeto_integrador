import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def requester(id_):
    return {"X-Requester-Id": str(id_)}


def criar_aacd(client, email):
    resposta = client.post("/users", json={"nome": "Teste", "email": email, "senha": "123456"})
    assert resposta.status_code == 201
    return resposta.get_json()["id"]


class Test_UpdateUserPresenter:
    def test_update_nome(self, client):
        uid = criar_aacd(client, "upd.nome@aacd.org.br")

        resposta = client.put(f"/users/{uid}", json={"nome": "Novo Nome"}, headers=requester(uid))

        assert resposta.status_code == 200
        assert resposta.get_json()["nome"] == "Novo Nome"
        assert "senha_hash" not in resposta.get_json()

        # persistiu: o get enxerga a mudança (mesmo repositório compartilhado)
        leitura = client.get(f"/users/{uid}", headers=requester(uid))
        assert leitura.get_json()["nome"] == "Novo Nome"

    def test_patch_also_works(self, client):
        uid = criar_aacd(client, "upd.patch@aacd.org.br")
        resposta = client.patch(f"/users/{uid}", json={"nome": "Via Patch"}, headers=requester(uid))
        assert resposta.status_code == 200
        assert resposta.get_json()["nome"] == "Via Patch"

    def test_update_other_user_is_forbidden(self, client):
        uid = criar_aacd(client, "upd.alvo@aacd.org.br")

        resposta = client.put(f"/users/{uid}", json={"nome": "Invasor"}, headers=requester(123))

        assert resposta.status_code == 403
        leitura = client.get(f"/users/{uid}", headers=requester(uid))
        assert leitura.get_json()["nome"] == "Teste"

    def test_update_user_not_found(self, client):
        resposta = client.put("/users/99999", json={"nome": "X"}, headers=requester(99999))
        assert resposta.status_code == 404

    def test_update_without_body(self, client):
        uid = criar_aacd(client, "upd.semcorpo@aacd.org.br")
        resposta = client.put(f"/users/{uid}", headers=requester(uid))
        assert resposta.status_code == 400

    def test_update_without_requester_header(self, client):
        uid = criar_aacd(client, "upd.semheader@aacd.org.br")
        resposta = client.put(f"/users/{uid}", json={"nome": "X"})
        assert resposta.status_code == 400