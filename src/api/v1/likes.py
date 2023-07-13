from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from auth.users import get_current_user
from broker_managers.views import ViewSerializerManager, get_view_manager
from models.likes import FilmLikes, FilmAverageScore, FilmEditScore

router = APIRouter()


@router.get(
    "/film-likes/{film_id}",
)
async def get_likes(
    film_id: UUID,
    # like_service: chto-to = Depends(some callable)
    ) -> FilmLikes:
    pass

@router.get(
    "/film-average/{film_id}",
)
async def get_likes(
    film_id: UUID,
    # like_service: chto-to = Depends(some callable)
    ) -> FilmAverageScore:
    pass


@router.get(
    "/movie-likes/{film_id}",
)
async def get_likes(
    film_id: UUID,
    # like_service: chto-to = Depends(some callable)
    ) -> FilmEditScore:
    pass