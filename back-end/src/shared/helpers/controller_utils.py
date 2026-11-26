from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import InvalidToken
from src.shared.helpers.token_handler import TokenHandler

def texto_obrigatorio(data: dict, campo: str) -> str:
    valor = data.get(campo)
    if valor is None:
        raise MissingParameters(campo)
    if not isinstance(valor, str):
        raise WrongTypeParameter(fieldName=campo, fieldTypeExpected=str,
                                 fieldTypeReceived=type(valor))
    if valor.strip() == "":
        raise MissingParameters(campo)
    return valor

def inteiro_obrigatorio(data: dict, campo: str) -> int:
    valor = data.get(campo)
    if valor is None:
        raise MissingParameters(campo)
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise WrongTypeParameter(fieldName=campo, fieldTypeExpected=int,
                                 fieldTypeReceived=type(valor))


def requester_id_obrigatorio(data: dict) -> int:
    """Lê o id de quem pede, de dentro do token (cabeçalho Authorization: Bearer <token>)."""
    autorizacao = None
    for chave, valor in data.items():                 # nomes de cabeçalho não diferenciam maiúsculas
        if isinstance(chave, str) and chave.lower() == "authorization":
            autorizacao = valor
            break

    if not isinstance(autorizacao, str):
        raise InvalidToken()

    partes = autorizacao.split(" ")
    if len(partes) != 2 or partes[0].lower() != "bearer" or not partes[1]:
        raise InvalidToken()

    return TokenHandler.decode(partes[1])