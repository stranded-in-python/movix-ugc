from http import HTTPStatus

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from config import settings
from managers import ViewSerializerManager, get_view_manager
from models import BasicViewEvent

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.post("/api/v1/ugc/events/view")
async def save_view(
    event: BasicViewEvent,
    view_manager: ViewSerializerManager = Depends(get_view_manager),
):
    if not await view_manager.save_to_storage(event):
        return HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Broker timed out."
        )
    return event


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["/app"]
    )
