from src.modules.user.app.login.login_viewmodel import LoginViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_LoginViewmodel:
    def test_to_dict(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash", role=RoleEnum.AACD)

        result = LoginViewmodel(user, "token_qualquer").to_dict()

        assert result["token"] == "token_qualquer"
        assert result["token_type"] == "Bearer"
        assert result["user"]["id"] == 1
        assert result["user"]["email"] == "ana@aacd.org.br"
        assert result["user"]["role"] == RoleEnum.AACD.value

    def test_never_returns_password(self):
        user = User(id=1, nome="Ana", email="ana@aacd.org.br",
                    senha_hash="hash_secreto", role=RoleEnum.AACD)

        result = LoginViewmodel(user, "token").to_dict()

        assert "senha_hash" not in str(result)
        assert "hash_secreto" not in str(result)