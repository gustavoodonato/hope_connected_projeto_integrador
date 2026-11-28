from flask import Flask, jsonify, request
from flask_cors import CORS

from src.modules.user.app.create_user.create_user_presenter import create_user_presenter
from src.modules.user.app.get_user.get_user_presenter import get_user_presenter
from src.modules.user.app.update_user.update_user_presenter import update_user_presenter
from src.modules.user.app.delete_user.delete_user_presenter import delete_user_presenter

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)  # libera o front (Live Server) a chamar o back-end

@app.route('/users/<user_id>', methods=["GET"])
def envioDados(user_id):
    return jsonify({'mensagem': 'Conexão Funcional!', 'status': 'OK'})

@app.route('/users', methods=["POST"])
def reciboDados():
    dadosRecebidos = request.get_json()
    nome = dadosRecebidos.get('nome')
    return jsonify({'resposta': f'Olá {nome}! Dados salvos!'})

app.add_url_rule("/users", "create_user", create_user_presenter, methods=["POST"])
app.add_url_rule("/users/<user_id>", "get_user", get_user_presenter, methods=["GET"])
#app.add_url_rule("/users", "get_all_users", get_all_users_presenter, methods=["GET"])
app.add_url_rule("/users/<user_id>", "update_user", update_user_presenter, methods=["PUT", "PATCH"])
app.add_url_rule("/users/<user_id>", "delete_user", delete_user_presenter, methods=["DELETE"])

if __name__ == "__main__":
    app.run(debug=True)