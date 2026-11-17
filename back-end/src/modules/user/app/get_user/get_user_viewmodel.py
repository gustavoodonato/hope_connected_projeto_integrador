from src.shared.domain.entities.user import User


class GetUserViewmodel:
    def __init__(self, user: User):
        self.id = user.id
        self.nome = user.nome
        self.email = user.email
        self.role = user.role.value
        self.phone = user.phone
        self.endereco = user.endereco.model_dump() if user.endereco else None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "endereco": self.endereco,
            "message": "Usuário encontrado com sucesso",
        }