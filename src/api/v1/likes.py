from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from models.likes import FilmAverageScore, FilmEditScore, FilmLikes
from services.likes import LikeServiceABC, get_like_service

router = APIRouter()


@router.get("/film-likes/")
async def get_likes(
    film_id: UUID, like_service: LikeServiceABC = Depends(get_like_service)
) -> FilmLikes:
    likes_and_dislikes = await like_service.get_likes(film_id)
    if not likes_and_dislikes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="film not found"
        )
    return likes_and_dislikes


@router.get("/film-average/")
async def get_average_score(
    film_id: UUID, like_service: LikeServiceABC = Depends(get_like_service)
) -> FilmAverageScore:
    average_score = await like_service.get_average_score_by_id(film_id)
    if not average_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="film not found"
        )
    return average_score


@router.post("/movie-score/")
async def post_score(
    film_id: UUID,
    user_id: UUID,
    score: int,
    like_service: LikeServiceABC = Depends(get_like_service),
) -> FilmEditScore:
    return await like_service.insert_film_score(user_id, film_id, score)


@router.patch("/movie-score/")
async def edit_score(
    film_id: UUID,
    user_id: UUID,
    score: int,
    like_service: LikeServiceABC = Depends(get_like_service),
) -> FilmEditScore:
    return await like_service.insert_film_score(user_id, film_id, score)


@router.delete("/movie-score/", response_model=None)
async def delete_score(
    film_id: UUID,
    user_id: UUID,
    like_service: LikeServiceABC = Depends(get_like_service),
) -> Response(status_code=status.HTTP_200_OK):
    await like_service.delete_film_score(user_id, film_id)
    return Response(status_code=status.HTTP_200_OK)
