from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import json
from app.logging.init_log import logger
from app.logging.log_context import set_request_id

class PostLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            body = await request.body()
            try:
                data = json.loads(body)
                request_id = data.get("request_id", "-")
            except Exception:
                data = body.decode("utf-8", errors="ignore")
                request_id = "-"

            set_request_id(str(request_id))
            logger.info(f"POST to {request.url.path} with body: {data}")

            request = Request(request.scope, receive=lambda: {"type": "http.request", "body": body})
            response = await call_next(request)

            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            text = response_body.decode("utf-8", errors="ignore")

            logger.info(f"Response from {request.url.path}: {text}")

            return Response(content=response_body,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            media_type=response.media_type)
        else:
            return await call_next(request)
