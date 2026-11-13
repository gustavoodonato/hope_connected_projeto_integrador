import pytest
from src.shared.domain.repositories.impressora_repository_interface import IImpressoraRepository
from src.shared.infra.repositories.impressora_repository_mock import ImpressoraRepositoryMock


class Test_IImpressoraRepository:
    def test_interface_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            IImpressoraRepository()

    def test_interface_contract(self):
        assert IImpressoraRepository.__abstractmethods__ == {
            "create_impressora",
            "get_impressora",
            "get_impressoras_by_fornecedor",
            "get_impressoras_disponiveis",
        }

    def test_mock_implements_interface(self):
        assert issubclass(ImpressoraRepositoryMock, IImpressoraRepository)
        assert isinstance(ImpressoraRepositoryMock(), IImpressoraRepository)
