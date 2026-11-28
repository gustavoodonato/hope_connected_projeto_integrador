from pydantic import BaseModel, Field, ConfigDict


class Arquivo3D(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    nome_original: str = Field(
        ...,
        description="Nome original do arquivo enviado"
    )

    chave_armazenamento: str = Field(
        ...,
        description="Identificador ou caminho do arquivo armazenado"
    )

    extensao: str = Field(
        ...,
        description="Extensão do arquivo 3D"
    )

    tamanho_bytes: int = Field(
        ...,
        gt=0,
        description="Tamanho do arquivo em bytes"
    )