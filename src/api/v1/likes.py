from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from auth.users import get_current_user
from broker_managers.views import ViewSerializerManager, get_view_manager
from models.likes import FilmLikes, FilmAverageScore, FilmEditScore, DeletedFilm

router = APIRouter()


@router.get(
    "/film-likes/",
)
async def get_likes(
    film_id: UUID,
    # like_service: chto-to = Depends(some callable)
    ) -> FilmLikes:
    pass

@router.get(
    "/film-average/",
)
async def get_average_score(
    film_id: UUID,
    # like_service: chto-to = Depends(some callable)
    ) -> FilmAverageScore:
    pass

@router.post(
    "/movie-score/",
)
async def get_l(
    film_id: UUID,
    user_id: UUID,
    score: int
    # like_service: chto-to = Depends(some callable)
    ) -> FilmEditScore:
    pass

@router.patch(
    "/movie-score/",
)
async def get_l(
    film_id: UUID,
    user_id: UUID,
    score: int
    # like_service: chto-to = Depends(some callable)
    ) -> FilmEditScore:
    pass

@router.delete(
    "/movie-score/",
)
async def get_l(
    film_id: UUID
    # like_service: chto-to = Depends(some callable)
    ) -> DeletedFilm:
    pass
