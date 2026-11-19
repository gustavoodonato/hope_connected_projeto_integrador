from flask import request
from src.modules.user.app.update_user.update_user_controller import UpdateUserController
from src.modules.user.app.update_user.update_user_usecase import UpdateUserUsecase
from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response

controller = UpdateUserController(UpdateUserUsecase(user_repo))

def update_user_presenter(user_id):
    response = controller(to_http_request(request, user_id=user_id))
    return to_flask_response(response)