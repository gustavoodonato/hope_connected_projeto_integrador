from flask import request

from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response
from src.modules.user.app.get_user.get_user_controller import GetUserController
from src.modules.user.app.get_user.get_user_usercase import GetUserUsecase

controller = GetUserController(GetUserUsecase(user_repo))


def get_user_presenter(user_id):
    http_request = to_http_request(request, user_id=user_id)
    response = controller(http_request)
    return to_flask_response(response)