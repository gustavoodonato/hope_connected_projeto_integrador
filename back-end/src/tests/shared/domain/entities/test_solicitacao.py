from datetime import datetime
import pytest
from pydantic import ValidationError
from src.shared.domain.entities.arquivo3d import Arquivo3D
from src.shared.domain.entities.solicitacao import Solicitacao
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.helpers.errors.domain_errors import EntityError


@pytest.fixture
def arquivo_3d():
    return Arquivo3D(
        nome_original="prototipo.stl",
        chave_armazenamento="solicitacoes/prototipo.stl",
        extensao=".stl",
        tamanho_bytes=1024,
    )


@pytest.fixture
def dados_validos(arquivo_3d):
    return dict(
        id_usuario_solicitante=123,
        id_usuario_destinatario=456,
        nome_peca="Prótese de mão",
        arquivo_3d=arquivo_3d,
    )


class Test_Solicitacao:
    def test_solicitacao_creation_success(self, arquivo_3d):
        data = datetime(2026, 11, 10, 9, 0, 0)
        solicitacao = Solicitacao(
            id=10,
            id_usuario_solicitante=123,
            id_usuario_destinatario=456,
            nome_peca="Prótese de mão",
            quantidade=3,
            prioridade=PrioridadeSolicitacaoEnum.ALTA,
            descricao="Prótese para uso diário",
            arquivo_3d=arquivo_3d,
            status=StatusSolicitacaoEnum.EM_PRODUCAO,
            data_criacao=data,
        )

        assert solicitacao.id == 10
        assert solicitacao.id_usuario_solicitante == 123
        assert solicitacao.id_usuario_destinatario == 456
        assert solicitacao.nome_peca == "Prótese de mão"
        assert solicitacao.quantidade == 3
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert solicitacao.descricao == "Prótese para uso diário"
        assert solicitacao.arquivo_3d == arquivo_3d
        assert solicitacao.status == StatusSolicitacaoEnum.EM_PRODUCAO
        assert solicitacao.data_criacao == data

    def test_solicitacao_default_values(self, dados_validos):
        antes = datetime.now()
        solicitacao = Solicitacao(**dados_validos)
        depois = datetime.now()

        assert solicitacao.id == 0
        assert solicitacao.quantidade == 1
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.MEDIA
        assert solicitacao.descricao is None
        assert solicitacao.status == StatusSolicitacaoEnum.ABERTO
        assert antes <= solicitacao.data_criacao <= depois

    def test_solicitacao_accepts_enum_values_as_string(self, dados_validos):
        solicitacao = Solicitacao(
            **dados_validos,
            prioridade="Alta",
            status="Em Produção",
        )
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert solicitacao.status == StatusSolicitacaoEnum.EM_PRODUCAO

    def test_solicitacao_nome_peca_is_stripped(self, dados_validos):
        dados_validos["nome_peca"] = "   Órtese de punho   "
        solicitacao = Solicitacao(**dados_validos)
        assert solicitacao.nome_peca == "Órtese de punho"

    @pytest.mark.parametrize("campo", ["id_usuario_solicitante", "id_usuario_destinatario"])
    def test_solicitacao_without_user_id(self, dados_validos, campo):
        del dados_validos[campo]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    @pytest.mark.parametrize("campo", ["id_usuario_solicitante", "id_usuario_destinatario"])
    @pytest.mark.parametrize("id_invalido", [0, -1])
    def test_solicitacao_invalid_user_id(self, dados_validos, campo, id_invalido):
        dados_validos[campo] = id_invalido
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_without_nome_peca(self, dados_validos):
        del dados_validos["nome_peca"]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_blank_nome_peca(self, dados_validos):
        dados_validos["nome_peca"] = "   "
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_nome_peca_too_long(self, dados_validos):
        dados_validos["nome_peca"] = "A" * 151
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    @pytest.mark.parametrize("quantidade_invalida", [0, -1])
    def test_solicitacao_invalid_quantidade(self, dados_validos, quantidade_invalida):
        dados_validos["quantidade"] = quantidade_invalida
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_invalid_prioridade(self, dados_validos):
        dados_validos["prioridade"] = "URGENTISSIMA"
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_invalid_status(self, dados_validos):
        dados_validos["status"] = "STATUS_INVALIDO"
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_without_arquivo_3d(self, dados_validos):
        del dados_validos["arquivo_3d"]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_accepts_arquivo_3d_as_dict(self):
        solicitacao = Solicitacao(
            id_usuario_solicitante=123,
            id_usuario_destinatario=456,
            nome_peca="Órtese",
            arquivo_3d={
                "nome_original": "ortese.stl",
                "chave_armazenamento": "solicitacoes/ortese.stl",
                "extensao": ".stl",
                "tamanho_bytes": 2048,
            },
        )
        assert isinstance(solicitacao.arquivo_3d, Arquivo3D)
        assert solicitacao.arquivo_3d.nome_original == "ortese.stl"

    def test_solicitacao_description_too_long(self, dados_validos):
        dados_validos["descricao"] = "A" * 1001
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_extra_field_forbidden(self, dados_validos):
        dados_validos["campo_inexistente"] = "x"
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_is_immutable(self, dados_validos):
        solicitacao = Solicitacao(**dados_validos)
        with pytest.raises(ValidationError):
            solicitacao.status = StatusSolicitacaoEnum.CANCELADO
