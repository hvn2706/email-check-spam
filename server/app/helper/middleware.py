import logging
from fastapi import Request
from starlette.responses import Response


_logger = logging.getLogger(__name__)


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        # if command request, then logging response
        if hasattr(request.state, 'trace_id'):
            trace_id = request.state.trace_id
            response_payload = b""
            async for chunk in response.body_iterator:
                response_payload += chunk

            try:
                response_http_code = response.status_code
                _logger.info(f"{trace_id} -- Response code {response_http_code}, payload: {response_payload}")
            except Exception as e:
                _logger.info(f"{trace_id} -- exception {str(e)}")

            return Response(
                content=response_payload,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        return response
    