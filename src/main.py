import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from config import settings
from models import BasicViewEvent
from services import ViewServiceABC, get_view_service

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.post("/api/v1/ugc/events/view")
async def save_view(
    event: BasicViewEvent, view_service: ViewServiceABC = Depends(get_view_service)
):
    event = await view_service.deserialize_to_binary(event)
    print(event)
    return event


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["/app"]
    )
