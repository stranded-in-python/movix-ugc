from asgi_correlation_id import CorrelationIdMiddleware
from ddtrace.contrib.asgi.middleware import TraceMiddleware
import structlog

from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from api.v1 import views
from core.config import settings
from core.logger import logging_middleware as _logging_middleware

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next) -> Response:
    await _logging_middleware(request, call_next)

app.add_middleware(CorrelationIdMiddleware)

tracing_middleware = next(
    (m for m in app.user_middleware if m.cls == TraceMiddleware), None
)
if tracing_middleware is not None:
    app.user_middleware = [m for m in app.user_middleware if m.cls != TraceMiddleware]
    structlog.stdlib.get_logger("api.datadog_patch").info(
        "Patching Datadog tracing middleware to be the outermost middleware..."
    )
    app.user_middleware.insert(0, tracing_middleware)
    app.middleware_stack = app.build_middleware_stack()

app.include_router(views.router, prefix="/api/v1/ugc/events", tags=["Views"])
