from abc import ABC, abstractmethod
from typing import List, Optional
from src.shared.domain.entities.impressora import Impressora
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum

class IImpressoraRepository(ABC):
    @abstractmethod
    def create_impressora(self, new_impressora: Impressora) -> Impressora:
        pass

    @abstractmethod
    def get_impressora(self, impressora_id: int) -> Impressora:
        """
        If impressora not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_impressoras_by_fornecedor(self, id_usuario_fornecedor: int) -> List[Impressora]:
        """
        Returns an empty list if the fornecedor has no impressoras
        """
        pass

    @abstractmethod
    def get_impressoras_disponiveis(self) -> List[Impressora]:
        """
        Returns only impressoras with status DISPONIVEL (catálogo que a AACD consulta)
        """
        pass

    @abstractmethod
    def update_impressora(
        self,
        impressora_id: int,
        marca_modelo: Optional[str] = None,
        tecnologia: Optional[TecnologiaImpressoraEnum] = None,
        volume_impressao: Optional[VolumeImpressao] = None,
        status_disponibilidade: Optional[StatusDisponibilidadeEnum] = None,
    ) -> Impressora:
        """
        Updates only the fields that were informed (None = keep current value).
        The owner (id_usuario_fornecedor) cannot be changed.
        If impressora not found raise NoItemsFound
        If the new values are invalid raise EntityError
        """
        pass

    @abstractmethod
    def delete_impressora(self, impressora_id: int) -> Impressora:
        """
        Returns the deleted impressora.
        If impressora not found raise NoItemsFound
        """
        pass
