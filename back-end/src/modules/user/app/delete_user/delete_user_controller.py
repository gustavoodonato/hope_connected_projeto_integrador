from src.modules.user.app.delete_user.delete_user_usecase import DeleteUserUsecase
from src.modules.user.app.delete_user.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError, NotFound, OK
from src.shared.helpers.controller_utils import inteiro_obrigatorio, requester_id_obrigatorio
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class DeleteUserController:
    def __init__(self, usecase: DeleteUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = inteiro_obrigatorio(request.data, "user_id")
            requester_id = requester_id_obrigatorio(request.data)

            user = self.usecase(user_id=user_id, requester_id=requester_id)

            return OK(DeleteUserViewmodel(user).to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))