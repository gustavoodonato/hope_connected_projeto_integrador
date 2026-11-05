from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

class Adress(BaseModel):
    cep: str = Field(
        ..., 
        description="Código de Endereçamento Postal", 
    )

    logradouro: str = Field(
        ..., 
        max_length=255
    )
    
    numero: str = Field(
        ..., 
        max_length=10
    )

    complemento: Optional[str] | None = Field(
        default=None, 
        max_length=100
    )

    bairro: str = Field(
        ..., 
        max_length=100
    )

    cidade: str = Field(
        ..., 
        max_length=100
    )

    estado: str = Field(
        ..., min_length=2, 
        max_length=2, 
        description="Sigla do estado (UF)"
    )

    @field_validator('cep')
    @classmethod
    def validar_e_limpar_cep(cls, v: str) -> str:
        cep_limpo = re.sub(r'\D', '', v)
        if len(cep_limpo) != 8:
            raise ValueError('O CEP deve conter exatamente 8 dígitos numéricos.')
        return cep_limpo

    @field_validator('estado')
    @classmethod
    def uf_maiuscula(cls, v: str) -> str:
        return v.upper()