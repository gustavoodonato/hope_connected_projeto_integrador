from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase
from src.modules.user.app.get_user.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import (
    BadRequest, Forbidden, InternalServerError, NotFound, OK, Unauthorized)
from src.shared.helpers.controller_utils import inteiro_obrigatorio, requester_id_obrigatorio
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidToken, NoItemsFound


class GetUserController:
    def __init__(self, usecase: GetUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = inteiro_obrigatorio(request.data, "user_id")
            requester_id = requester_id_obrigatorio(request.data)

            user = self.usecase(user_id=user_id, requester_id=requester_id)

            return OK(GetUserViewmodel(user).to_dict())

        except InvalidToken as err:
            return Unauthorized(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))