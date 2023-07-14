from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import likes, views
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(views.router, prefix="/api/v1/ugc/events", tags=["Views"])
app.include_router(likes.router, prefix="/api/v1/ugc", tags=["UGC"])
