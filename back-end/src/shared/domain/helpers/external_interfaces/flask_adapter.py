from flask import Request, Response, jsonify, make_response

from src.shared.helpers.external_interfaces.external_interface import IResponse
from src.shared.helpers.external_interfaces.http_model import HttpRequest


def to_http_request(flask_request: Request, **url_params) -> HttpRequest:
    """Flask request -> HttpRequest. url_params são valores da URL (ex.: user_id)."""
    body = flask_request.get_json(silent=True)
    query_params = {**flask_request.args.to_dict(), **url_params}
    return HttpRequest(
        body=body if isinstance(body, dict) else {},
        headers=dict(flask_request.headers),
        query_params=query_params,
    )


def to_flask_response(response: IResponse) -> Response:
    """IResponse -> resposta do Flask."""
    if response.status_code in (204, 304):
        flask_response = make_response("", response.status_code)
    else:
        flask_response = make_response(jsonify(response.body), response.status_code)
    for key, value in response.headers.items():
        flask_response.headers[key] = value
    return flask_response