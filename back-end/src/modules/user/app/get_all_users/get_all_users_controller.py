from src.modules.user.app.get_all_users.get_all_users_usecase import GetAllUsersUsecase
from src.modules.user.app.get_all_users.get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError, OK, Unauthorized
from src.shared.helpers.controller_utils import requester_id_obrigatorio
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidToken


class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            requester_id = requester_id_obrigatorio(request.data)

            users = self.usecase(requester_id=requester_id)

            return OK(GetAllUsersViewmodel(users).to_dict())

        except InvalidToken as err:
            return Unauthorized(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))