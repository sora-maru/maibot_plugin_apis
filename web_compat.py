"""Request-scoped objects used by the ported controller. No HTTP server."""
from contextvars import ContextVar
import json


class Query(dict):
    def getlist(self, name):
        value = self.get(name, [])
        return value if isinstance(value, list) else [value]


class Request:
    def __init__(self, method="GET", params=None, payload=None):
        self.method = method
        self.query = Query(params or {})
        self.payload = payload or {}
        self.content_type = "application/json"

    async def json(self, default=None):
        return dict(self.payload)

    async def body(self):
        return json.dumps(self.payload).encode()


current_request = ContextVar("apis_web_request")


class RequestProxy:
    def __getattr__(self, name):
        return getattr(current_request.get(), name)


request = RequestProxy()


class Response:
    def __init__(self, content, media_type="application/octet-stream", status_code=200):
        self.content = content.encode("utf-8") if isinstance(content, str) else content
        self.media_type = media_type
        self.status_code = status_code
        self.headers = {}


def json_response(data, status_code=200):
    return data


def error_response(message, status_code=400, data=None):
    return {"status": "error", "message": str(message), "data": data or {}}


class StreamResponse:
    def __init__(self, generator):
        self.generator = generator


def stream_response(generator, **kwargs):
    return StreamResponse(generator)
