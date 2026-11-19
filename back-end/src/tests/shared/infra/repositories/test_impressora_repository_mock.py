import pytest
from src.shared.domain.entities.impressora import Impressora
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.impressora_repository_mock import ImpressoraRepositoryMock


def nova_impressora() -> Impressora:
    return Impressora(
        id_usuario_fornecedor=789,
        marca_modelo="Prusa MK4",
        tecnologia=TecnologiaImpressoraEnum.FDM,
        volume_impressao=VolumeImpressao(x_mm=250, y_mm=210, z_mm=220),
    )


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

        criada = repo.create_impressora(nova_impressora())

        assert criada.id == 4
        assert len(repo.impressoras) == 4
        assert repo.impressoras[-1].marca_modelo == "Prusa MK4"
        assert repo.get_impressora(4).id_usuario_fornecedor == 789

    def test_create_impressora_appears_in_catalogs(self):
        repo = ImpressoraRepositoryMock()

        repo.create_impressora(nova_impressora())

        assert [i.id for i in repo.get_impressoras_by_fornecedor(789)] == [3, 4]
        assert [i.id for i in repo.get_impressoras_disponiveis()] == [1, 3, 4]

    def test_update_impressora_status(self):
        repo = ImpressoraRepositoryMock()

        atualizada = repo.update_impressora(
            impressora_id=1,
            status_disponibilidade=StatusDisponibilidadeEnum.INATIVA,
        )

        assert atualizada.id == 1
        assert atualizada.status_disponibilidade == StatusDisponibilidadeEnum.INATIVA
        assert repo.get_impressora(1).status_disponibilidade == StatusDisponibilidadeEnum.INATIVA

    def test_update_impressora_keeps_fields_not_informed(self):
        repo = ImpressoraRepositoryMock()

        atualizada = repo.update_impressora(impressora_id=1, marca_modelo="Creality Ender 3 S1")

        assert atualizada.marca_modelo == "Creality Ender 3 S1"
        assert atualizada.id_usuario_fornecedor == 456
        assert atualizada.tecnologia == TecnologiaImpressoraEnum.FDM
        assert atualizada.volume_impressao.x_mm == 220
        assert atualizada.status_disponibilidade == StatusDisponibilidadeEnum.DISPONIVEL

    def test_update_impressora_all_fields(self):
        repo = ImpressoraRepositoryMock()

        atualizada = repo.update_impressora(
            impressora_id=1,
            marca_modelo="Elegoo Saturn",
            tecnologia=TecnologiaImpressoraEnum.SLA,
            volume_impressao=VolumeImpressao(x_mm=218, y_mm=123, z_mm=250),
            status_disponibilidade=StatusDisponibilidadeEnum.EM_USO,
        )

        assert atualizada.marca_modelo == "Elegoo Saturn"
        assert atualizada.tecnologia == TecnologiaImpressoraEnum.SLA
        assert atualizada.volume_impressao.y_mm == 123
        assert atualizada.status_disponibilidade == StatusDisponibilidadeEnum.EM_USO
        assert atualizada.id_usuario_fornecedor == 456

    def test_update_impressora_does_not_change_list_size_or_order(self):
        repo = ImpressoraRepositoryMock()

        repo.update_impressora(impressora_id=2, marca_modelo="Novo nome")

        assert [i.id for i in repo.impressoras] == [1, 2, 3]
        assert repo.impressoras[1].marca_modelo == "Novo nome"

    def test_update_impressora_removes_from_disponiveis(self):
        repo = ImpressoraRepositoryMock()

        repo.update_impressora(impressora_id=1, status_disponibilidade=StatusDisponibilidadeEnum.EM_USO)

        assert [i.id for i in repo.get_impressoras_disponiveis()] == [3]

    def test_update_impressora_not_found(self):
        repo = ImpressoraRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.update_impressora(impressora_id=999, marca_modelo="Qualquer")

    def test_update_impressora_invalid_value_keeps_original(self):
        repo = ImpressoraRepositoryMock()

        with pytest.raises(EntityError):
            repo.update_impressora(impressora_id=1, marca_modelo="   ")

        assert repo.get_impressora(1).marca_modelo == "Creality Ender 3 V2"

    def test_delete_impressora(self):
        repo = ImpressoraRepositoryMock()

        removida = repo.delete_impressora(1)

        assert removida.id == 1
        assert removida.marca_modelo == "Creality Ender 3 V2"
        assert len(repo.impressoras) == 2
        with pytest.raises(NoItemsFound):
            repo.get_impressora(1)

    def test_delete_impressora_removes_from_catalogs(self):
        repo = ImpressoraRepositoryMock()

        repo.delete_impressora(1)

        assert [i.id for i in repo.get_impressoras_by_fornecedor(456)] == [2]
        assert [i.id for i in repo.get_impressoras_disponiveis()] == [3]

    def test_delete_impressora_not_found(self):
        repo = ImpressoraRepositoryMock()
        with pytest.raises(NoItemsFound):
            repo.delete_impressora(impressora_id=999)
        assert len(repo.impressoras) == 3
