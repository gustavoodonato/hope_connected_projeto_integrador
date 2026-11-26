from datetime import datetime, timedelta, timezone

import jwt
import pytest

from src.shared.helpers.errors.usecase_errors import InvalidToken
from src.shared.helpers.token_handler import TokenHandler


class Test_TokenHandler:
    def test_generate_and_decode(self):
        token = TokenHandler.generate(456)
        assert isinstance(token, str)
        assert TokenHandler.decode(token) == 456

    def test_different_users_get_different_tokens(self):
        assert TokenHandler.generate(1) != TokenHandler.generate(2)

    def test_expired_token(self):
        token = TokenHandler.generate(456, expira_em_minutos=-1)
        with pytest.raises(InvalidToken):
            TokenHandler.decode(token)

    def test_tampered_token(self):
        header, payload, assinatura = TokenHandler.generate(456).split(".")
        adulterado = ".".join([header, payload[:-2] + "xx", assinatura])
        with pytest.raises(InvalidToken):
            TokenHandler.decode(adulterado)

    def test_token_signed_with_another_key(self):
        futuro = datetime.now(timezone.utc) + timedelta(minutes=5)
        falso = jwt.encode({"sub": "456", "exp": futuro}, "outra-chave-qualquer-com-32-caracteres!", algorithm="HS256")
        with pytest.raises(InvalidToken):
            TokenHandler.decode(falso)

    @pytest.mark.parametrize("lixo", ["", "abc", "a.b.c", "Bearer xyz"])
    def test_garbage_token(self, lixo):
        with pytest.raises(InvalidToken):
            TokenHandler.decode(lixo)