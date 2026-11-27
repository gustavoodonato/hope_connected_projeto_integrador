from abc import ABC, abstractmethod
from typing import List, Optional
from src.shared.domain.entities.solicitacao import Solicitacao
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum

class ISolicitacaoRepository(ABC):
    @abstractmethod
    def create_solicitacao(self, new_solicitacao: Solicitacao) -> Solicitacao:
        pass

    @abstractmethod
    def get_solicitacao(self, solicitacao_id: int) -> Solicitacao:
        """
        If solicitacao not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_solicitacoes_by_usuario_aacd(self, id_usuario_aacd: int) -> List[Solicitacao]:
        """
        Returns an empty list if the usuario has no solicitacoes
        """
        pass

    @abstractmethod
    def get_solicitacoes_abertas(self) -> List[Solicitacao]:
        """
        Returns only solicitacoes with status ABERTO (pedidos que os fornecedores podem aceitar)
        """
        pass

    @abstractmethod
    def update_solicitacao(
        self,
        solicitacao_id: int,
        nome_peca: Optional[str] = None,
        material_requerido: Optional[str] = None,
        quantidade: Optional[int] = None,
        prioridade: Optional[PrioridadeSolicitacaoEnum] = None,
        status: Optional[StatusSolicitacaoEnum] = None,
    ) -> Solicitacao:
        """
        Updates only the fields that were informed (None = keep current value).
        The owner (id_usuario_aacd) and data_criacao cannot be changed.
        If solicitacao not found raise NoItemsFound
        If the new values are invalid raise EntityError
        """
        pass

    @abstractmethod
    def delete_solicitacao(self, solicitacao_id: int) -> Solicitacao:
        """
        Returns the deleted solicitacao.
        If solicitacao not found raise NoItemsFound
        """
        pass
