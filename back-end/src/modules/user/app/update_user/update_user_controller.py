from pydantic import ValidationError

from src.modules.user.app.update_user.update_user_usecase import UpdateUserUsecase
from src.modules.user.app.update_user.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.adress import Adress
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import BadRequest, Forbidden, InternalServerError, NotFound, OK, Unauthorized
from src.shared.helpers.controller_utils import inteiro_obrigatorio, requester_id_obrigatorio
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidToken, NoItemsFound


class UpdateUserController:
    def __init__(self, usecase: UpdateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            user_id = inteiro_obrigatorio(request.data, "user_id")
            requester_id = requester_id_obrigatorio(request.data)

            nome = request.data.get("nome")
            phone = request.data.get("phone")
            dados_endereco = request.data.get("endereco")
            endereco = None

            if nome is not None:
                if not isinstance(nome, str):
                    raise WrongTypeParameter(fieldName="nome", fieldTypeExpected=str,
                                             fieldTypeReceived=type(nome))
                if nome.strip() == "":
                    raise EntityError("nome")

            if phone is not None and not isinstance(phone, str):
                raise WrongTypeParameter(fieldName="phone", fieldTypeExpected=str,
                                         fieldTypeReceived=type(phone))

            if dados_endereco is not None:
                if not isinstance(dados_endereco, dict):
                    raise WrongTypeParameter(fieldName="endereco", fieldTypeExpected=dict,
                                             fieldTypeReceived=type(dados_endereco))
                endereco = Adress(**dados_endereco)

            if nome is None and phone is None and endereco is None:
                raise MissingParameters("nome, phone ou endereco")

            user = self.usecase(
                user_id=user_id,
                requester_id=requester_id,
                nome=nome,
                phone=phone,
                endereco=endereco,
            )

            return OK(UpdateUserViewmodel(user).to_dict())

        except InvalidToken as err:
            return Unauthorized(body=err.message)

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except ValidationError:
            return BadRequest(body="endereco inválido")

        except Exception as err:
            return InternalServerError(body=str(err))