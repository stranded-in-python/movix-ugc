from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from models.reviews import Review, ReviewLikes
from services.reviews import ReviewServiceABC, get_review_service

router = APIRouter()


@router.post("/review/")
async def post_review(
    user_id: UUID,
    film_id: UUID,
    text: str,
    score: Annotated[
        int,
        Path(title="Score of how you liked the movie. 10-like, 0-dislike", ge=1, le=10),
    ],
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> Review:
    return await review_service.insert_review(user_id, film_id, text, score)


@router.post("/review-score/")
async def post_review_score(
    user_id: UUID,
    review_id: UUID,
    score: Annotated[
        int,
        Path(
            title="Score of how you liked the review. 10-like, 0-dislike", ge=1, le=10
        ),
    ],
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> ReviewLikes:
    return await review_service.insert_review_score(user_id, review_id, score)


@router.get("/reviews/", response_model=None)
async def get_reviews(
    film_id: UUID,
    sort: str | None = None,
    review_service: ReviewServiceABC = Depends(get_review_service),
) -> list[Review]:
    reviews = await review_service.get_reviews(film_id, sort)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="reviews not found"
        )
    return reviews
