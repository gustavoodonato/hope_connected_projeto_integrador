from enum import Enum

class StatusDisponibilidadeEnum(str, Enum):
    DISPONIVEL = "Disponível"
    EM_USO = "Em Uso"
    INATIVA = "Inativa"
