from fastapi import APIRouter, Depends, HTTPException, status

from managers.users import get_current_user
from managers.views import ViewSerializerManager, get_view_manager
from models.models import BasicViewEvent, UserViewEvent

router = APIRouter()


@router.post(
    "/view",
    response_model=BasicViewEvent,
    summary="View event",
    description="Post view event",
    response_description="id, user_id, film_id, view's timestamp, frame of a movie",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Broker timed out."},
    },
)
async def save_view(
    event: UserViewEvent,
    user=Depends(get_current_user),
    view_manager: ViewSerializerManager = Depends(get_view_manager),
) -> BasicViewEvent:
    if not await view_manager.save_to_storage(event):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Broker timed out."
        )
    return event
