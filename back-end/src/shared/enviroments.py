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

    @staticmethod
    def get_impressora_repo():
        if Enviroments.stage == "TEST":
            from src.shared.infra.repositories.impressora_repository_mock import ImpressoraRepositoryMock
            return ImpressoraRepositoryMock
        raise NotImplementedError("Repositório de produção ainda não criado")

    @staticmethod
    def get_solicitacao_repo():
        if Enviroments.stage == "TEST":
            from src.shared.infra.repositories.solicitacao_repository_mock import SolicitacaoRepositoryMock
            return SolicitacaoRepositoryMock
        raise NotImplementedError("Repositório de produção ainda não criado")
