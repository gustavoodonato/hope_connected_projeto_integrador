from pydantic import ValidationError
from src.shared.domain.entities.adress import Adress
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.domain.helpers.external_interfaces.http_codes import BadRequest, Conflict, Created, InternalServerError
from src.modules.user.app.create_user.create_user_usecase import CreateUserUsecase
from src.modules.user.app.create_user.create_user_viewmodel import CreateUserViewmodel


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            nome = request.data.get('nome', None)
            email = request.data.get('email', None)
            senha = request.data.get('senha', None)
            phone = request.data.get('phone', None)
            dados_endereco = request.data.get('endereco', None)
            endereco = None

            if nome is None:
                raise MissingParameters('nome')
            if type(nome) != str:
                raise WrongTypeParameter(fieldName='nome', fieldTypeExpected=str, fieldTypeReceived=type(nome))

            if email is None:
                raise MissingParameters('email')
            if type(email) != str:
                raise WrongTypeParameter(fieldName='email', fieldTypeExpected=str, fieldTypeReceived=type(email))

            if senha is None:
                raise MissingParameters('senha')
            if type(senha) != str:
                raise WrongTypeParameter(fieldName='senha', fieldTypeExpected=str, fieldTypeReceived=type(senha))

            if phone is not None and not isinstance(phone, str):
                raise WrongTypeParameter(fieldName='phone', fieldTypeExpected=str, fieldTypeReceived=type(phone))

            if dados_endereco is not None:
                if not isinstance(dados_endereco, dict):
                    raise WrongTypeParameter(fieldName='endereco', fieldTypeExpected=dict, fieldTypeReceived=type(dados_endereco))
                endereco = Adress(**dados_endereco)

            user = self.usecase(
                nome=nome,
                email=email,
                senha=senha,
                phone=phone,
                endereco=endereco
            )

            viewmodel = CreateUserViewmodel(user)
            return Created(viewmodel.to_dict())

        except DuplicatedItem as err:
            return Conflict(body=err.message)

        except (MissingParameters, WrongTypeParameter, EntityError) as err:
            return BadRequest(body=err.message)

        except ValidationError:
            return BadRequest(body="endereco inválido")

        except Exception as err:
            return InternalServerError(body=str(err))