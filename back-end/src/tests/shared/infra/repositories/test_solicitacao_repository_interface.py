import pytest
from src.shared.domain.repositories.solicitacao_repository_interface import ISolicitacaoRepository
from src.shared.infra.repositories.solicitacao_repository_mock import SolicitacaoRepositoryMock


class Test_ISolicitacaoRepository:
    def test_interface_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            ISolicitacaoRepository()

    def test_interface_contract(self):
        assert ISolicitacaoRepository.__abstractmethods__ == {
            "create_solicitacao",
            "get_solicitacao",
            "get_solicitacoes_by_usuario_aacd",
            "get_solicitacoes_abertas",
            "update_solicitacao",
            "delete_solicitacao",
        }

    def test_mock_implements_interface(self):
        assert issubclass(SolicitacaoRepositoryMock, ISolicitacaoRepository)
        assert isinstance(SolicitacaoRepositoryMock(), ISolicitacaoRepository)
