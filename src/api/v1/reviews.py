from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.users import get_current_user
from core.predefined import LikeDislike
from models.reviews import Review, ReviewLikes
from models.models import User
from services.reviews import ReviewServiceABC, get_review_service

router = APIRouter()


@router.post("/review/")
async def post_review(
    user_id: UUID,
    film_id: UUID,
    text: str,
    score: Annotated[
        int,
        Query(
            title="Score of how you liked the movie. 10-like, 0-dislike", ge=1, le=10
        ),
    ],
    user_creds: User, user=Depends(get_current_user),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> Review:
    return await review_service.insert_review(user_id, film_id, text, score)


@router.post("/review/score/")
async def post_review_score(
    user_id: UUID,
    review_id: UUID,
    score: LikeDislike,
    user_creds: User, user=Depends(get_current_user),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> ReviewLikes:
    return await review_service.insert_review_score(user_id, review_id, score)


@router.get("/reviews/", response_model=None)
async def get_reviews(
    film_id: UUID,
    user_creds: User,
    sort: str | None = None,
    user=Depends(get_current_user),
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> list[Review]:
    reviews = await review_service.get_reviews(film_id, sort)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="reviews not found"
        )
    return reviews
