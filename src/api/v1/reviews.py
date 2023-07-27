from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.users import get_current_user
from core.pagination import PaginateQueryParams
from core.predefined import LikeDislike
from models.reviews import Review, ReviewLikes
from services.reviews import ReviewServiceABC, get_review_service

router = APIRouter()


@router.post(
    "/review/",
    response_model=Review,
    summary="Post a new review",
    description="Post a new review of a movie",
    response_description="user_id, film_id, review text, your score",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def post_review(
    film_id: UUID,
    text: str,
    score: Annotated[
        int,
        Query(
            title="Score of how you liked the movie. 10-like, 0-dislike", ge=1, le=10
        ),
    ],
    user=Depends(get_current_user),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> Review:
    return await review_service.insert_review(user.user_id, film_id, text, score)


@router.post(
    "/review/score/",
    response_model=ReviewLikes,
    summary="Post a score of a review",
    description="Post a like or dislike of others review",
    response_description="user_id, review_id, your score",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def post_review_score(
    review_id: UUID,
    score: LikeDislike,
    user=Depends(get_current_user),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> ReviewLikes:
    return await review_service.insert_review_score(user.user_id, review_id, score)


@router.get(
    "/reviews/",
    response_model=None,
    summary="Get reviews",
    description="Get reviews of a movie",
    response_description="film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Reviews not found."},
    },
)
async def get_reviews(
    film_id: UUID,
    sort: str | None = None,
    user=Depends(get_current_user),
    pagination: PaginateQueryParams = Depends(PaginateQueryParams),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> list[Review]:
    reviews = await review_service.get_reviews(film_id, sort, pagination)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reviews not found."
        )
    return reviews
