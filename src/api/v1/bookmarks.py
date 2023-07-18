from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from models.bookmarks import Bookmark, ShortBookmark
from services.bookmarks import BookmarkServiceABC, get_bookmark_service

router = APIRouter()

@router.post("/bookmark/")
async def post_bookmark(
    user_id: UUID, film_id: UUID, bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service)
) -> Bookmark:
    return await bookmark_service.insert_bookmark(user_id, film_id)

@router.delete("/bookmark/", response_model=None)
async def delete_bookmark(
    film_id: UUID, user_id: UUID, bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service)
) -> Response(status_code=status.HTTP_200_OK):
    await bookmark_service.delete_bookmark(user_id, film_id)
    return Response(status_code=status.HTTP_200_OK)

@router.get("/bookmarks/", response_model=None)
async def get_bookmarks(
    user_id: UUID, bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service)
) -> list[ShortBookmark]:
    bookmarks = await bookmark_service.get_bookmarks(user_id)
    if not bookmarks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bookmarks not found")
    return bookmarks
