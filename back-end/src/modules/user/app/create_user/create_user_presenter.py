from flask import request

from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response
from src.modules.user.app.create_user.create_user_controller import CreateUserController
from src.modules.user.app.create_user.create_user_usecase import CreateUserUsecase

controller = CreateUserController(CreateUserUsecase(user_repo))


def create_user_presenter():
    http_request = to_http_request(request)
    response = controller(http_request)
    return to_flask_response(response)