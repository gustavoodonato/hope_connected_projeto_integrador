from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError, model_validator
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.entities.adress import Adress

class User(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            loc = err.errors()[0]["loc"]
            campo = str(loc[0]) if loc else "user"
            raise EntityError(campo) from err

    id: int = Field(
        default_factory=int,
        description="Id unico do usuário"
    )

    nome: str =  Field(
        ...,
        description="Nome do usuário"
    )

    email: EmailStr = Field(
        ...,
        description="Email do usuário"
    )

    senha_hash: str = Field (
        ..., 
        description="Senha hash de usuário"
    )

    phone: Optional[str] = Field (
        default=None,
        description="Telefone do usuário"
    )

    endereco: Optional[Adress] = Field (
        default=None,
        description="Endereço do usuário"
    )
    role: RoleEnum = Field(
        ...,
        description="Role do usuário"
    )


    @model_validator(mode="after")
    def validar_campos_do_fornecedor(self):
        if self.role == RoleEnum.FORNECEDOR:
            if not self.phone or not self.endereco:
                raise ValueError("Fornecedor precisa de telefone e endereço")
        return self