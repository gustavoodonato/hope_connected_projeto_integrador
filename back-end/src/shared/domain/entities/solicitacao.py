from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.entities.arquivo3d import Arquivo3D

class Solicitacao(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            loc = err.errors()[0]["loc"]
            campo = str(loc[0]) if loc else "solicitacao"
            raise EntityError(campo) from err

    id: int = Field(
        default=0,
        description="Id único da solicitação"
    )

    id_usuario_solicitante: int = Field(
        ...,
        gt=0
    )

    id_usuario_destinatario: int = Field(
        ...,
        gt=0
    )

    nome_peca: str = Field(
        ...,
        max_length=150
    )

    quantidade: int = Field(
        default=1,
        gt=0
    )

    prioridade: PrioridadeSolicitacaoEnum = Field(
        default=PrioridadeSolicitacaoEnum.MEDIA
    )

    descricao: str | None = Field(
        default=None,
        max_length=1000
    )

    arquivo_3d: Arquivo3D = Field(
        ...
    )

    status: StatusSolicitacaoEnum = Field(
        default=StatusSolicitacaoEnum.ABERTO
    )

    data_criacao: datetime = Field(
        default_factory=datetime.now
    )

    @field_validator('nome_peca')
    @classmethod
    def validar_texto_obrigatorio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("campo de texto não pode ser vazio")
        return v