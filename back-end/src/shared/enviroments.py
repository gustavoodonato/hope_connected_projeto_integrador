import os

class Environments:
    stage = os.environ.get("STAGE", "TEST")

    @staticmethod
    def get_user_repo():
        if Environments.stage == "TEST":
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock
        raise NotImplementedError("Repositório de produção ainda não criado")

    @staticmethod
    def get_impressora_repo():
        if Environments.stage == "TEST":
            from src.shared.infra.repositories.impressora_repository_mock import ImpressoraRepositoryMock
            return ImpressoraRepositoryMock
        raise NotImplementedError("Repositório de produção ainda não criado")
