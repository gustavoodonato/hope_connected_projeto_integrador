from pydantic import BaseModel, ConfigDict, Field


class VolumeImpressao(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    x_mm: float = Field(
        ...,
        gt=0,
        description="Largura útil da mesa de impressão, em milímetros"
    )

    y_mm: float = Field(
        ...,
        gt=0,
        description="Profundidade útil da mesa de impressão, em milímetros"
    )

    z_mm: float = Field(
        ...,
        gt=0,
        description="Altura máxima de impressão, em milímetros"
    )
