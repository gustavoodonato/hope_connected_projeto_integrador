from flask import request
from src.modules.user.app.login.login_controller import LoginController
from src.modules.user.app.login.login_usecase import LoginUsecase
from src.shared.dependencies import user_repo
from src.shared.domain.helpers.external_interfaces.flask_adapter import to_http_request, to_flask_response
from src.shared.helpers.auth import auth



controller = LoginController(LoginUsecase(user_repo))

def login_presenter():
    response = controller(to_http_request(request))
    return to_flask_response(response)

def requester(id_):
    return auth(id_)