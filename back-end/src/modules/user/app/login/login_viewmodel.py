from src.shared.domain.entities.user import User


class LoginViewmodel:
    def __init__(self, user: User, token: str):
        self.token = token
        self.id = user.id
        self.nome = user.nome
        self.email = user.email
        self.role = user.role.value

    def to_dict(self):
        return {
            "token": self.token,
            "token_type": "Bearer",
            "user": {
                "id": self.id,
                "nome": self.nome,
                "email": self.email,
                "role": self.role,
            },
            "message": "Login realizado com sucesso",
        }