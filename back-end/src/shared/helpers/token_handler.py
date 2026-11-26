from datetime import datetime, timedelta, timezone

import jwt

from src.shared.enviroments import Enviroments
from src.shared.helpers.errors.usecase_errors import InvalidToken

algorithm = "HS256"
expiracao_minutos = 60


class TokenHandler:
    @staticmethod
    def generate(user_id: int, expira_em_minutos: int = expiracao_minutos) -> str:
        agora = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": agora,
            "exp": agora + timedelta(minutes=expira_em_minutos),
        }
        return jwt.encode(payload, Enviroments.secret_key, algorithm=algorithm)

    @staticmethod
    def decode(token: str) -> int:
        try:
            payload = jwt.decode(token, Enviroments.secret_key, algorithms=[algorithm])
            return int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, ValueError):
            raise InvalidToken()