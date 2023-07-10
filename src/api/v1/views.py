from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from managers.views import ViewSerializerManager, get_view_manager
from models.models import BasicViewEvent


router = APIRouter()


@router.post("/view")
async def save_view(
    event: BasicViewEvent,
    view_manager: ViewSerializerManager = Depends(get_view_manager),
):
    if not await view_manager.save_to_storage(event):
        return HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Broker timed out."
        )
    return event
