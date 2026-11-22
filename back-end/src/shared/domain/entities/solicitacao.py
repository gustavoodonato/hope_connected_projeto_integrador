from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from src.shared.domain.enums.prioridade_solicitacao_enum import PrioridadeSolicitacaoEnum
from src.shared.domain.enums.status_solicitacao_enum import StatusSolicitacaoEnum
from src.shared.helpers.errors.domain_errors import EntityError


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
        default_factory=int,
        description="Id unico da solicitação"
    )

    id_usuario_aacd: int = Field(
        ...,
        gt=0,
        description="Id do usuário da AACD que criou a solicitação"
    )

    nome_peca: str = Field(
        ...,
        max_length=150,
        description="Nome da peça (órtese ou prótese) solicitada"
    )

    material_requerido: str = Field(
        ...,
        max_length=60,
        description="Material exigido para a impressão (ex: PLA, PETG, ABS)"
    )

    quantidade: int = Field(
        default=1,
        gt=0,
        description="Quantidade de peças solicitadas"
    )

    prioridade: PrioridadeSolicitacaoEnum = Field(
        default=PrioridadeSolicitacaoEnum.MEDIA,
        description="Prioridade da solicitação"
    )

    status: StatusSolicitacaoEnum = Field(
        default=StatusSolicitacaoEnum.ABERTO,
        description="Status da solicitação"
    )

    data_criacao: datetime = Field(
        default_factory=datetime.now,
        description="Data e hora de criação da solicitação"
    )

    @field_validator('nome_peca', 'material_requerido')
    @classmethod
    def validar_texto_obrigatorio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("campo de texto não pode ser vazio")
        return v
