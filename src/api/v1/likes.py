from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from auth.users import get_current_user
from models import likes as model_likes
from services.likes import LikeServiceABC, get_like_service

router = APIRouter()


@router.get(
    "/film/likes/",
    response_model=model_likes.FilmLikes,
    summary="Get likes",
    description="Get movie likes and dislikes",
    response_description="film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def get_likes(
    film_id: UUID,
    user=Depends(get_current_user),
    like_service: LikeServiceABC = Depends(get_like_service),
) -> model_likes.FilmLikes:
    return await like_service.get_likes(film_id)


@router.get(
    "/film/score/average/",
    response_model=model_likes.FilmAverageScore,
    summary="Get an average score",
    description="Get an average score of a movie",
    response_description="film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Movie not found."},
    },
)
async def get_average_score(
    film_id: UUID,
    user=Depends(get_current_user),
    like_service: LikeServiceABC = Depends(get_like_service),
) -> model_likes.FilmAverageScore:
    average_score = await like_service.get_average_score_by_id(film_id)
    if not average_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found."
        )
    return average_score


@router.post(
    "/film/score/",
    response_model=model_likes.FilmEditScore,
    summary="Post a new score",
    description="Post a new score of a movie",
    response_description="user_id, film_id, score (from 0 to 10)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def post_score(
    score: Annotated[int, Query(title="Score of how you liked the movie", ge=1, le=10)],
    film_id: UUID,
    user=Depends(get_current_user),
    like_service: LikeServiceABC = Depends(get_like_service),
) -> model_likes.FilmEditScore:
    return await like_service.insert_film_score(user.user_id, film_id, score)


@router.patch(
    "/film/score/",
    response_model=model_likes.FilmEditScore,
    summary="Edit a score",
    description="Edit a score of a movie",
    response_description="user_id, film_id, score (from 0 to 10)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def edit_score(
    film_id: UUID,
    score: Annotated[int, Query(title="Score of how you liked the movie", ge=1, le=10)],
    user=Depends(get_current_user),
    like_service: LikeServiceABC = Depends(get_like_service),
) -> model_likes.FilmEditScore:
    return await like_service.insert_film_score(user.user_id, film_id, score)


@router.delete(
    "/film/score/",
    response_model=None,
    summary="Delete a score",
    description="Delete a score of a movie",
    response_description="user_id, film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def delete_score(
    film_id: UUID,
    user=Depends(get_current_user),
    like_service: LikeServiceABC = Depends(get_like_service),
) -> Response(status_code=status.HTTP_200_OK):
    await like_service.delete_film_score(user.user_id, film_id)
    return Response(status_code=status.HTTP_200_OK)
