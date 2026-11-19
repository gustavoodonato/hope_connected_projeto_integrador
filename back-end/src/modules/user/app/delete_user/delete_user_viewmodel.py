from src.shared.domain.entities.user import User

class DeleteUserViewmodel:
    def __init__(self, user: User):
        self.id = user.id
        self.nome = user.nome
        self.email = user.email

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "message": "Usuário removido com sucesso",
        }