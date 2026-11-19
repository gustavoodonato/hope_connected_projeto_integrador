from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter

REQUESTER_HEADER = "X-Requester-Id"

def inteiro_obrigatorio(data: dict, campo: str) -> int:
    valor = data.get(campo)
    if valor is None:
        raise MissingParameters(campo)
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise WrongTypeParameter(fieldName=campo, fieldTypeExpected=int, fieldTypeReceived=type(valor))

def requester_id_obrigatorio(data: dict) -> int:
    return inteiro_obrigatorio(data, REQUESTER_HEADER)