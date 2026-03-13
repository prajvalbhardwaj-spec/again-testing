import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        client_ip = request.headers.get("x-forwarded-for", None)
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.critical(
                "%s %s | IP: %s | %.2fms | 500 | UNHANDLED: %s",
                request.method,
                request.url.path,
                client_ip,
                elapsed,
                repr(exc),
                exc_info=True,
            )
            raise

        elapsed = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code

        if status_code >= 500:
            log_fn = logger.error
        elif status_code == 404:
            log_fn = logger.warning
        elif status_code >= 400:
            log_fn = logger.warning
        else:
            log_fn = logger.info

        log_fn(
            "%s %s | IP: %s | %.2fms | %s",
            request.method,
            request.url.path,
            client_ip,
            elapsed,
            status_code,
        )

        return response
