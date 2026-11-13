from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.impressora import Impressora

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
