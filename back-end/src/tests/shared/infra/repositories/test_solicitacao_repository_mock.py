from datetime import datetime

import pytest
from src.shared.domain.entities.solicitacao import Solicitacao
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.solicitacao_repository_mock import SolicitacaoRepositoryMock


def nova_solicitacao(id_usuario_aacd: int = 321) -> Solicitacao:
    return Solicitacao(
        id_usuario_aacd=id_usuario_aacd,
        nome_peca="Órtese de tornozelo",
        material_requerido="TPU",
        quantidade=2,
        prioridade=PrioridadeSolicitacaoEnum.ALTA,
    )


class Test_SolicitacaoRepositoryMock:
    def test_get_solicitacao(self):
        repo = SolicitacaoRepositoryMock()
        solicitacao = repo.get_solicitacao(1)

        assert solicitacao.id == 1
        assert solicitacao.id_usuario_aacd == 123
        assert solicitacao.nome_peca == "Prótese de mão"
        assert solicitacao.material_requerido == "PLA"
        assert solicitacao.quantidade == 2
        assert solicitacao.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert solicitacao.status == StatusSolicitacaoEnum.ABERTO
        assert solicitacao.data_criacao == datetime(2026, 11, 10, 9, 0, 0)

    def test_get_solicitacao_accepts_id_as_string(self):
        repo = SolicitacaoRepositoryMock()
        assert repo.get_solicitacao("3").nome_peca == "Suporte de dedo"

    def test_get_solicitacao_not_found(self):
        repo = SolicitacaoRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_solicitacao(solicitacao_id=999)

    def test_get_solicitacoes_by_usuario_aacd(self):
        repo = SolicitacaoRepositoryMock()
        solicitacoes = repo.get_solicitacoes_by_usuario_aacd(123)

        assert [s.id for s in solicitacoes] == [1, 2, 3]
        assert all(s.id_usuario_aacd == 123 for s in solicitacoes)

    def test_get_solicitacoes_by_usuario_aacd_without_solicitacoes(self):
        repo = SolicitacaoRepositoryMock()
        assert repo.get_solicitacoes_by_usuario_aacd(999) == []

    def test_get_solicitacoes_abertas(self):
        repo = SolicitacaoRepositoryMock()
        solicitacoes = repo.get_solicitacoes_abertas()

        assert [s.id for s in solicitacoes] == [1, 3]
        assert all(s.status == StatusSolicitacaoEnum.ABERTO for s in solicitacoes)

    def test_create_solicitacao(self):
        repo = SolicitacaoRepositoryMock()

        criada = repo.create_solicitacao(nova_solicitacao())

        assert criada.id == 4
        assert len(repo.solicitacoes) == 4
        assert repo.solicitacoes[-1].nome_peca == "Órtese de tornozelo"
        assert repo.get_solicitacao(4).id_usuario_aacd == 321

    def test_create_solicitacao_appears_in_catalogs(self):
        repo = SolicitacaoRepositoryMock()

        repo.create_solicitacao(nova_solicitacao(id_usuario_aacd=321))

        assert [s.id for s in repo.get_solicitacoes_by_usuario_aacd(321)] == [4]
        assert [s.id for s in repo.get_solicitacoes_by_usuario_aacd(123)] == [1, 2, 3]
        assert [s.id for s in repo.get_solicitacoes_abertas()] == [1, 3, 4]

    def test_update_solicitacao_status(self):
        repo = SolicitacaoRepositoryMock()

        atualizada = repo.update_solicitacao(
            solicitacao_id=1,
            status=StatusSolicitacaoEnum.EM_PRODUCAO,
        )

        assert atualizada.id == 1
        assert atualizada.status == StatusSolicitacaoEnum.EM_PRODUCAO
        assert repo.get_solicitacao(1).status == StatusSolicitacaoEnum.EM_PRODUCAO

    def test_update_solicitacao_keeps_fields_not_informed(self):
        repo = SolicitacaoRepositoryMock()

        atualizada = repo.update_solicitacao(solicitacao_id=1, quantidade=10)

        assert atualizada.quantidade == 10
        assert atualizada.id_usuario_aacd == 123
        assert atualizada.nome_peca == "Prótese de mão"
        assert atualizada.material_requerido == "PLA"
        assert atualizada.prioridade == PrioridadeSolicitacaoEnum.ALTA
        assert atualizada.status == StatusSolicitacaoEnum.ABERTO
        assert atualizada.data_criacao == datetime(2026, 11, 10, 9, 0, 0)

    def test_update_solicitacao_all_fields(self):
        repo = SolicitacaoRepositoryMock()

        atualizada = repo.update_solicitacao(
            solicitacao_id=1,
            nome_peca="Prótese de antebraço",
            material_requerido="ABS",
            quantidade=4,
            prioridade=PrioridadeSolicitacaoEnum.BAIXA,
            status=StatusSolicitacaoEnum.CANCELADO,
        )

        assert atualizada.nome_peca == "Prótese de antebraço"
        assert atualizada.material_requerido == "ABS"
        assert atualizada.quantidade == 4
        assert atualizada.prioridade == PrioridadeSolicitacaoEnum.BAIXA
        assert atualizada.status == StatusSolicitacaoEnum.CANCELADO
        assert atualizada.id_usuario_aacd == 123

    def test_update_solicitacao_does_not_change_list_size_or_order(self):
        repo = SolicitacaoRepositoryMock()

        repo.update_solicitacao(solicitacao_id=2, nome_peca="Novo nome")

        assert [s.id for s in repo.solicitacoes] == [1, 2, 3]
        assert repo.solicitacoes[1].nome_peca == "Novo nome"

    def test_update_solicitacao_removes_from_abertas(self):
        repo = SolicitacaoRepositoryMock()

        repo.update_solicitacao(solicitacao_id=1, status=StatusSolicitacaoEnum.EM_PRODUCAO)

        assert [s.id for s in repo.get_solicitacoes_abertas()] == [3]

    def test_update_solicitacao_not_found(self):
        repo = SolicitacaoRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.update_solicitacao(solicitacao_id=999, nome_peca="Qualquer")

    @pytest.mark.parametrize("campo, valor", [("nome_peca", "   "), ("quantidade", 0)])
    def test_update_solicitacao_invalid_value_keeps_original(self, campo, valor):
        repo = SolicitacaoRepositoryMock()

        with pytest.raises(EntityError):
            repo.update_solicitacao(solicitacao_id=1, **{campo: valor})

        original = repo.get_solicitacao(1)
        assert original.nome_peca == "Prótese de mão"
        assert original.quantidade == 2

    def test_delete_solicitacao(self):
        repo = SolicitacaoRepositoryMock()

        removida = repo.delete_solicitacao(1)

        assert removida.id == 1
        assert removida.nome_peca == "Prótese de mão"
        assert len(repo.solicitacoes) == 2
        with pytest.raises(NoItemsFound):
            repo.get_solicitacao(1)

    def test_delete_solicitacao_removes_from_catalogs(self):
        repo = SolicitacaoRepositoryMock()

        repo.delete_solicitacao(1)

        assert [s.id for s in repo.get_solicitacoes_by_usuario_aacd(123)] == [2, 3]
        assert [s.id for s in repo.get_solicitacoes_abertas()] == [3]

    def test_delete_solicitacao_not_found(self):
        repo = SolicitacaoRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_solicitacao(solicitacao_id=999)
        assert len(repo.solicitacoes) == 3
