import os

class Enviroments:
    secret_key = os.environ.get("SECRET_KEY", "chave-somente-para-desenvolvimento-local-0000")
    stage = os.environ.get("STAGE", "TEST")

    @staticmethod
    def get_user_repo():
        if Enviroments.stage == "TEST":
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        raise NotImplementedError("Repositório de produção ainda não criado") 