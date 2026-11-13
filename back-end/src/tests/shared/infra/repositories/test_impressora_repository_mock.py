import pytest
from src.shared.domain.entities.impressora import Impressora
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.impressora_repository_mock import ImpressoraRepositoryMock


class Test_ImpressoraRepositoryMock:
    def test_get_impressora(self):
        repo = ImpressoraRepositoryMock()
        impressora = repo.get_impressora(1)

        assert impressora.id == 1
        assert impressora.id_usuario_fornecedor == 456
        assert impressora.marca_modelo == "Creality Ender 3 V2"
        assert impressora.tecnologia == TecnologiaImpressoraEnum.FDM
        assert impressora.volume_impressao.x_mm == 220
        assert impressora.status_disponibilidade == StatusDisponibilidadeEnum.DISPONIVEL

    def test_get_impressora_accepts_id_as_string(self):
        repo = ImpressoraRepositoryMock()
        assert repo.get_impressora("3").marca_modelo == "Bambu Lab P1S"

    def test_get_impressora_not_found(self):
        repo = ImpressoraRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.get_impressora(impressora_id=999)

    def test_get_impressoras_by_fornecedor(self):
        repo = ImpressoraRepositoryMock()
        impressoras = repo.get_impressoras_by_fornecedor(456)

        assert [i.id for i in impressoras] == [1, 2]
        assert all(i.id_usuario_fornecedor == 456 for i in impressoras)

    def test_get_impressoras_by_fornecedor_without_impressoras(self):
        repo = ImpressoraRepositoryMock()
        assert repo.get_impressoras_by_fornecedor(999) == []

    def test_get_impressoras_disponiveis(self):
        repo = ImpressoraRepositoryMock()
        impressoras = repo.get_impressoras_disponiveis()

        assert [i.id for i in impressoras] == [1, 3]
        assert all(
            i.status_disponibilidade == StatusDisponibilidadeEnum.DISPONIVEL
            for i in impressoras
        )

    def test_create_impressora(self):
        repo = ImpressoraRepositoryMock()
        impressora = Impressora(
            id_usuario_fornecedor=789,
            marca_modelo="Prusa MK4",
            tecnologia=TecnologiaImpressoraEnum.FDM,
            volume_impressao=VolumeImpressao(x_mm=250, y_mm=210, z_mm=220),
        )

        criada = repo.create_impressora(impressora)

        assert criada.id == 4
        assert len(repo.impressoras) == 4
        assert repo.impressoras[-1].marca_modelo == "Prusa MK4"
        assert repo.get_impressora(4).id_usuario_fornecedor == 789

    def test_create_impressora_appears_in_catalogs(self):
        repo = ImpressoraRepositoryMock()
        impressora = Impressora(
            id_usuario_fornecedor=789,
            marca_modelo="Prusa MK4",
            tecnologia=TecnologiaImpressoraEnum.FDM,
            volume_impressao=VolumeImpressao(x_mm=250, y_mm=210, z_mm=220),
        )

        repo.create_impressora(impressora)

        assert [i.id for i in repo.get_impressoras_by_fornecedor(789)] == [3, 4]
        assert [i.id for i in repo.get_impressoras_disponiveis()] == [1, 3, 4]
