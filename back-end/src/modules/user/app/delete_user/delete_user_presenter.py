from flask import request
from src.modules.user.app.delete_user.delete_user_controller import DeleteUserController
from src.modules.user.app.delete_user.delete_user_usecase import DeleteUserUsecase
from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response
from src.shared.helpers.auth import auth

controller = DeleteUserController(DeleteUserUsecase(user_repo))

def delete_user_presenter(user_id):
    response = controller(to_http_request(request, user_id=user_id))
    return to_flask_response(response)

def requester(id_):
    return auth(id_)