
import pytest
from pydantic import ValidationError

from src.shared.domain.entities.arquivo3d import Arquivo3D


@pytest.fixture
def dados_validos():
    return dict(
        nome_original="prototipo.stl",
        chave_armazenamento="solicitacoes/prototipo.stl",
        extensao=".stl",
        tamanho_bytes=1024,
    )


class Test_Arquivo3D:
    def test_arquivo3d_creation_success(self):
        arquivo = Arquivo3D(
            nome_original="modelo.stl",
            chave_armazenamento="solicitacoes/modelo.stl",
            extensao=".stl",
            tamanho_bytes=2048,
        )

        assert arquivo.nome_original == "modelo.stl"
        assert arquivo.chave_armazenamento == "solicitacoes/modelo.stl"
        assert arquivo.extensao == ".stl"
        assert arquivo.tamanho_bytes == 2048

    def test_arquivo3d_missing_required_field(self, dados_validos):
        for campo in ("nome_original", "chave_armazenamento", "extensao", "tamanho_bytes"):
            dados = dados_validos.copy()
            del dados[campo]

            with pytest.raises(ValidationError):
                Arquivo3D(**dados)

    @pytest.mark.parametrize("tamanho_invalido", [0, -1])
    def test_arquivo3d_invalid_tamanho_bytes(self, dados_validos, tamanho_invalido):
        dados_validos["tamanho_bytes"] = tamanho_invalido

        with pytest.raises(ValidationError):
            Arquivo3D(**dados_validos)

    def test_arquivo3d_extra_field_forbidden(self, dados_validos):
        dados_validos["campo_inexistente"] = "x"

        with pytest.raises(ValidationError):
            Arquivo3D(**dados_validos)

    def test_arquivo3d_is_immutable(self, dados_validos):
        arquivo = Arquivo3D(**dados_validos)

        with pytest.raises(ValidationError):
            arquivo.extensao = ".obj"
