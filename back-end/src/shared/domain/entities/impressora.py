from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Impressora(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            loc = err.errors()[0]["loc"]
            campo = str(loc[0]) if loc else "impressora"
            raise EntityError(campo) from err

    id: int = Field(
        default_factory=int,
        description="Id unico da impressora"
    )

    id_usuario_fornecedor: int = Field(
        ...,
        gt=0,
        description="Id do usuário fornecedor dono da impressora"
    )

    marca_modelo: str = Field(
        ...,
        max_length=120,
        description="Marca e modelo da impressora (ex: Creality Ender 3 V2)"
    )

    tecnologia: TecnologiaImpressoraEnum = Field(
        ...,
        description="Tecnologia de impressão (FDM, SLA, ...)"
    )

    volume_impressao: VolumeImpressao = Field(
        ...,
        description="Volume máximo de impressão, em milímetros"
    )

    status_disponibilidade: StatusDisponibilidadeEnum = Field(
        default=StatusDisponibilidadeEnum.DISPONIVEL,
        description="Status de disponibilidade da impressora"
    )

    @field_validator('marca_modelo')
    @classmethod
    def validar_marca_modelo(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("marca_modelo não pode ser vazio")
        return v
