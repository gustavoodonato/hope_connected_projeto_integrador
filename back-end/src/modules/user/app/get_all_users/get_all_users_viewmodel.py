from typing import List
from src.shared.domain.entities.user import User

class GetAllUsersViewmodel:
    def __init__(self, users: List[User]):
        self.users = [
            {
                "id": u.id,
                "nome": u.nome,
                "cidade": u.endereco.cidade if u.endereco else None,
                "estado": u.endereco.estado if u.endereco else None,
            }
            for u in users
        ]

    def to_dict(self):
        return {
            "users": self.users,
            "total": len(self.users),
            "message": "Usuários encontrados com sucesso",
        }