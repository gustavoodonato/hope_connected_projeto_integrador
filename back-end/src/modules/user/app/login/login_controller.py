from src.modules.user.app.login.login_usecase import LoginUsecase
from src.modules.user.app.login.login_viewmodel import LoginViewmodel
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import (
    BadRequest, InternalServerError, OK, Unauthorized)
from src.shared.helpers.controller_utils import texto_obrigatorio
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import WrongCredentials
from src.shared.helpers.token_handler import TokenHandler


class LoginController:
    def __init__(self, usecase: LoginUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            email = texto_obrigatorio(request.data, "email")
            senha = texto_obrigatorio(request.data, "senha")

            user = self.usecase(email=email, senha=senha)
            token = TokenHandler.generate(user.id)

            return OK(LoginViewmodel(user, token).to_dict())

        except WrongCredentials as err:
            return Unauthorized(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))