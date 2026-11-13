from typing import List
from src.shared.domain.entities.impressora import Impressora
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum
from src.shared.domain.repositories.impressora_repository_interface import IImpressoraRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class ImpressoraRepositoryMock(IImpressoraRepository):
    impressoras: List[Impressora]

    def __init__(self):
        # id_usuario_fornecedor 456 (Lucas) e 789 (Julio) existem no UserRepositoryMock
        self.impressoras = [
            Impressora(
                id=1,
                id_usuario_fornecedor=456,
                marca_modelo="Creality Ender 3 V2",
                tecnologia=TecnologiaImpressoraEnum.FDM,
                volume_impressao=VolumeImpressao(x_mm=220, y_mm=220, z_mm=250),
                status_disponibilidade=StatusDisponibilidadeEnum.DISPONIVEL,
            ),
            Impressora(
                id=2,
                id_usuario_fornecedor=456,
                marca_modelo="Anycubic Photon Mono X",
                tecnologia=TecnologiaImpressoraEnum.SLA,
                volume_impressao=VolumeImpressao(x_mm=192, y_mm=120, z_mm=245),
                status_disponibilidade=StatusDisponibilidadeEnum.EM_USO,
            ),
            Impressora(
                id=3,
                id_usuario_fornecedor=789,
                marca_modelo="Bambu Lab P1S",
                tecnologia=TecnologiaImpressoraEnum.FDM,
                volume_impressao=VolumeImpressao(x_mm=256, y_mm=256, z_mm=256),
                status_disponibilidade=StatusDisponibilidadeEnum.DISPONIVEL,
            ),
        ]

    def create_impressora(self, new_impressora: Impressora) -> Impressora:
        novo_id = max((i.id for i in self.impressoras), default=0) + 1
        impressora = new_impressora.model_copy(update={"id": novo_id})
        self.impressoras.append(impressora)
        return impressora

    def get_impressora(self, impressora_id: int) -> Impressora:
        for impressora in self.impressoras:
            if str(impressora.id) == str(impressora_id):
                return impressora
        raise NoItemsFound("impressora_id")

    def get_impressoras_by_fornecedor(self, id_usuario_fornecedor: int) -> List[Impressora]:
        return [
            i for i in self.impressoras
            if str(i.id_usuario_fornecedor) == str(id_usuario_fornecedor)
        ]

    def get_impressoras_disponiveis(self) -> List[Impressora]:
        return [
            i for i in self.impressoras
            if i.status_disponibilidade == StatusDisponibilidadeEnum.DISPONIVEL
        ]
