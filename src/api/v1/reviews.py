from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from models.reviews import Review, ReviewLikes
from services.reviews import ReviewServiceABC, get_review_service

router = APIRouter()

@router.post("/review/")
async def post_review(
    user_id: UUID, film_id: UUID, text: str, score: int, review_service: ReviewServiceABC = Depends(get_review_service)
) -> Review:
    return await review_service.insert_review(user_id, film_id, text, score)

@router.post("/review-score/", # response_model=None
             )
async def post_review_score(
    user_id: UUID, review_id: UUID, score: int, review_service: ReviewServiceABC = Depends(get_review_service)
) -> ReviewLikes:
    return await review_service.insert_review_score(user_id, review_id, score)

# @router.get("/reviews/", response_model=None)
# async def get_bookmarks(
#     user_id: UUID, review_service: ReviewServiceABC = Depends(get_review_service)
# ) -> ?????:
#     pass
