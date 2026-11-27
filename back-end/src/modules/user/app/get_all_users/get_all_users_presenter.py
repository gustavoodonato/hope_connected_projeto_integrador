from flask import request
from src.modules.user.app.get_all_users.get_all_users_controller import GetAllUsersController
from src.modules.user.app.get_all_users.get_all_users_usecase import GetAllUsersUsecase
from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response

controller = GetAllUsersController(GetAllUsersUsecase(user_repo))

def get_all_users_presenter():
    response = controller(to_http_request(request))
    return to_flask_response(response)