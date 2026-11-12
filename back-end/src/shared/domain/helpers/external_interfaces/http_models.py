from typing import Any, Optional
from warnings import warn

from src.shared.domain.helpers.external_interfaces.external_interface import IRequest, IResponse

class HttpRequest(IRequest):
    """Junta body, headers e query_params em um único dicionário `data`.
    Em chaves repetidas, vale a ordem: body < headers < query_params."""

    def __init__(self, body: Any = None, headers: Optional[dict] = None,
                 query_params: Optional[dict] = None):
        self.body = body if body is not None else {}
        self.headers = headers or {}
        self.query_params = query_params or {}

        data_dict = {}
        if isinstance(self.body, dict):
            data_dict.update(self.body)
        elif isinstance(self.body, str):
            data_dict["body"] = self.body

        body_keys = self.body.keys() if isinstance(self.body, dict) else []
        overlapping = [k for k in body_keys if k in self.headers or k in self.query_params]
        overlapping += [k for k in self.query_params if k in self.headers]
        if overlapping:
            warn(f"body, query_params and/or headers have overlapping keys → {overlapping}")

        data_dict.update(self.headers)
        data_dict.update(self.query_params)
        self.data = data_dict

    def __repr__(self):
        return (f"HttpRequest (body={self.body}, headers={self.headers}, "
                f"query_params={self.query_params}, data={self.data})")


class HttpResponse(IResponse):
    def __init__(self, status_code: int, body: Any = None,
                 headers: Optional[dict] = None, data: Optional[dict] = None):
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body if body is not None else (data or {})

        data_dict = {}
        if isinstance(self.body, dict):
            data_dict.update(self.body)
        elif isinstance(self.body, str):
            data_dict["body"] = self.body

        data_dict.update(self.headers)
        self.data = data_dict

    def __repr__(self):
        return (f"HttpResponse (status_code={self.status_code}, "
                f"body={self.body}, headers={self.headers})")