from datetime import datetime

import pytest
from pydantic import ValidationError

from src.shared.domain.entities.solicitacao import Solicitacao
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.helpers.errors.domain_errors import EntityError


@pytest.fixture
def dados_validos():
    return dict(
        id_usuario_aacd=123,
        nome_peca="Prótese de mão",
        material_requerido="PLA",
    )


class Test_Solicitacao:
    def test_solicitacao_creation_success(self):
        data = datetime(2026, 11, 10, 9, 0, 0)
        solicitacao = Solicitacao(
            id=10,
            id_usuario_aacd=123,
            nome_peca="Prótese de mão",
            material_requerido="PLA",
            quantidade=3,
            prioridade=PrioridadeSolicitacaoEnum.ALTA,
            status=StatusSolicitacaoEnum.EM_PRODUCAO,
            data_criacao=data,
        )
        assert solicitacao.id == 10
        assert solicitacao.id_usuario_aacd == 123
        assert solicitacao.nome_peca == "Prótese de mão"
        assert solicitacao.material_requerido == "PLA"
        assert solicitacao.quantidade == 3
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert solicitacao.status == StatusSolicitacaoEnum.EM_PRODUCAO
        assert solicitacao.data_criacao == data

    def test_solicitacao_default_values(self, dados_validos):
        antes = datetime.now()
        solicitacao = Solicitacao(**dados_validos)
        depois = datetime.now()

        assert solicitacao.id == 0
        assert solicitacao.quantidade == 1
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.MEDIA
        assert solicitacao.status == StatusSolicitacaoEnum.ABERTO
        assert antes <= solicitacao.data_criacao <= depois

    def test_solicitacao_accepts_enum_values_as_string(self, dados_validos):
        solicitacao = Solicitacao(**dados_validos, prioridade="Alta", status="Em Produção")
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert solicitacao.status == StatusSolicitacaoEnum.EM_PRODUCAO

    def test_solicitacao_text_fields_are_stripped(self, dados_validos):
        dados_validos["nome_peca"] = "   Órtese de punho   "
        dados_validos["material_requerido"] = "  PETG  "
        solicitacao = Solicitacao(**dados_validos)
        assert solicitacao.nome_peca == "Órtese de punho"
        assert solicitacao.material_requerido == "PETG"

    def test_solicitacao_without_id_usuario_aacd(self, dados_validos):
        del dados_validos["id_usuario_aacd"]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    @pytest.mark.parametrize("id_invalido", [0, -1])
    def test_solicitacao_invalid_id_usuario_aacd(self, dados_validos, id_invalido):
        dados_validos["id_usuario_aacd"] = id_invalido
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_without_nome_peca(self, dados_validos):
        del dados_validos["nome_peca"]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_blank_nome_peca(self, dados_validos):
        dados_validos["nome_peca"] = "    "
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_nome_peca_too_long(self, dados_validos):
        dados_validos["nome_peca"] = "A" * 151
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_without_material_requerido(self, dados_validos):
        del dados_validos["material_requerido"]
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_blank_material_requerido(self, dados_validos):
        dados_validos["material_requerido"] = "    "
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_material_requerido_too_long(self, dados_validos):
        dados_validos["material_requerido"] = "A" * 61
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    @pytest.mark.parametrize("quantidade_invalida", [0, -3])
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

    def test_solicitacao_extra_field_forbidden(self, dados_validos):
        dados_validos["campo_inexistente"] = "x"
        with pytest.raises(EntityError):
            Solicitacao(**dados_validos)

    def test_solicitacao_is_immutable(self, dados_validos):
        solicitacao = Solicitacao(**dados_validos)
        with pytest.raises(ValidationError):
            solicitacao.status = StatusSolicitacaoEnum.CANCELADO
