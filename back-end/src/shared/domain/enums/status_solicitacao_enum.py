from enum import Enum

class StatusSolicitacaoEnum(str, Enum):
    ABERTO = "Aberto"
    EM_PRODUCAO = "Em Produção"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"
