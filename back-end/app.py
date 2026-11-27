from flask import Flask
from flask_cors import CORS
from src.modules.user.app.login.login_presenter import login_presenter
from src.modules.user.app.create_user.create_user_presenter import create_user_presenter
from src.modules.user.app.get_user.get_user_presenter import get_user_presenter
from src.modules.user.app.get_all_users.get_all_users_presenter import get_all_users_presenter
from src.modules.user.app.update_user.update_user_presenter import update_user_presenter
from src.modules.user.app.delete_user.delete_user_presenter import delete_user_presenter

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

app.add_url_rule("/users", "create_user", create_user_presenter, methods=["POST"])
app.add_url_rule("/users/<user_id>", "get_user", get_user_presenter, methods=["GET"])
app.add_url_rule("/users", "get_all_users", get_all_users_presenter, methods=["GET"])
app.add_url_rule("/users/<user_id>", "update_user", update_user_presenter, methods=["PUT", "PATCH"])
app.add_url_rule("/users/<user_id>", "delete_user", delete_user_presenter, methods=["DELETE"])
app.add_url_rule("/login", "login", login_presenter, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)