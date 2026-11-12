from src.shared.domain.entities.user import User

class CreateUserViewmodel():
    def __init__(self, user: User):
        self.id = user.id
        self.nome = user.nome
        self.email = user.email
        self.phone = user.phone
        self.endereco = user.endereco
        self.role = user.role

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "phone": self.phone,
            "endereco": self.endereco,
            "role": self.role,
            "message": "User criado com sucesso"
        }