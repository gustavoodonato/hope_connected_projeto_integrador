from datetime import datetime
from typing import List, Optional
from src.shared.domain.entities.solicitacao import Solicitacao
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.domain.repositories.solicitacao_repository_interface import ISolicitacaoRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class SolicitacaoRepositoryMock(ISolicitacaoRepository):
    solicitacoes: List[Solicitacao]

    def __init__(self):
        # id_usuario_aacd 123 (Murilo) é o usuário AACD do UserRepositoryMock
        self.solicitacoes = [
            Solicitacao(
                id=1,
                id_usuario_aacd=123,
                nome_peca="Prótese de mão",
                material_requerido="PLA",
                quantidade=2,
                prioridade=PrioridadeSolicitacaoEnum.ALTA,
                status=StatusSolicitacaoEnum.ABERTO,
                data_criacao=datetime(2026, 11, 10, 9, 0, 0),
            ),
            Solicitacao(
                id=2,
                id_usuario_aacd=123,
                nome_peca="Órtese de punho",
                material_requerido="PETG",
                quantidade=1,
                prioridade=PrioridadeSolicitacaoEnum.MEDIA,
                status=StatusSolicitacaoEnum.EM_PRODUCAO,
                data_criacao=datetime(2026, 11, 11, 14, 30, 0),
            ),
            Solicitacao(
                id=3,
                id_usuario_aacd=123,
                nome_peca="Suporte de dedo",
                material_requerido="PLA",
                quantidade=5,
                prioridade=PrioridadeSolicitacaoEnum.BAIXA,
                status=StatusSolicitacaoEnum.ABERTO,
                data_criacao=datetime(2026, 11, 12, 10, 15, 0),
            ),
        ]

    def create_solicitacao(self, new_solicitacao: Solicitacao) -> Solicitacao:
        novo_id = max((s.id for s in self.solicitacoes), default=0) + 1
        solicitacao = new_solicitacao.model_copy(update={"id": novo_id})
        self.solicitacoes.append(solicitacao)
        return solicitacao

    def get_solicitacao(self, solicitacao_id: int) -> Solicitacao:
        for solicitacao in self.solicitacoes:
            if str(solicitacao.id) == str(solicitacao_id):
                return solicitacao
        raise NoItemsFound("solicitacao_id")

    def get_solicitacoes_by_usuario_aacd(self, id_usuario_aacd: int) -> List[Solicitacao]:
        return [
            s for s in self.solicitacoes
            if str(s.id_usuario_aacd) == str(id_usuario_aacd)
        ]

    def get_solicitacoes_abertas(self) -> List[Solicitacao]:
        return [
            s for s in self.solicitacoes
            if s.status == StatusSolicitacaoEnum.ABERTO
        ]

    def update_solicitacao(
        self,
        solicitacao_id: int,
        nome_peca: Optional[str] = None,
        material_requerido: Optional[str] = None,
        quantidade: Optional[int] = None,
        prioridade: Optional[PrioridadeSolicitacaoEnum] = None,
        status: Optional[StatusSolicitacaoEnum] = None,
    ) -> Solicitacao:
        solicitacao_atual = self.get_solicitacao(solicitacao_id)

        novos_valores = {
            "nome_peca": nome_peca,
            "material_requerido": material_requerido,
            "quantidade": quantidade,
            "prioridade": prioridade,
            "status": status,
        }
        novos_valores = {k: v for k, v in novos_valores.items() if v is not None}

        # recria a entidade (em vez de model_copy) para validar os novos valores
        solicitacao_atualizada = Solicitacao(**{**solicitacao_atual.model_dump(), **novos_valores})

        indice = self.solicitacoes.index(solicitacao_atual)
        self.solicitacoes[indice] = solicitacao_atualizada
        return solicitacao_atualizada

    def delete_solicitacao(self, solicitacao_id: int) -> Solicitacao:
        solicitacao = self.get_solicitacao(solicitacao_id)
        self.solicitacoes.remove(solicitacao)
        return solicitacao
