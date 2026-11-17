from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase
from src.modules.user.app.get_user.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError, NotFound, OK
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound

REQUESTER_HEADER = "X-Requester-Id"


class GetUserController:
    def __init__(self, usecase: GetUserUsecase):
        self.usecase = usecase

    @staticmethod
    def _inteiro_obrigatorio(data: dict, campo: str) -> int:
        valor = data.get(campo)
        if valor is None:
            raise MissingParameters(campo)
        try:
            return int(valor)
        except (TypeError, ValueError):
            raise WrongTypeParameter(fieldName=campo, fieldTypeExpected=int,
                                     fieldTypeReceived=type(valor))

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = self._inteiro_obrigatorio(request.data, "user_id")
            requester_id = self._inteiro_obrigatorio(request.data, REQUESTER_HEADER)

            user = self.usecase(user_id=user_id, requester_id=requester_id)

            return OK(GetUserViewmodel(user).to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))