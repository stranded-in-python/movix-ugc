from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth.users import get_current_user
from models.bookmarks import Bookmark, ShortBookmark
from services.bookmarks import BookmarkServiceABC, get_bookmark_service

router = APIRouter()


@router.post(
    "/bookmark/",
    response_model=Bookmark,
    summary="Post bookmark",
    description="Make a new bookmark",
    response_description="user_id, film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def post_bookmark(
    film_id: UUID,
    user=Depends(get_current_user),
    bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service),
) -> Bookmark:
    return await bookmark_service.insert_bookmark(user.user_id, film_id)


@router.delete(
    "/bookmark/",
    response_model=None,
    summary="Delete bookmark",
    description="Delete a bookmark",
    response_description="user_id, film_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
)
async def delete_bookmark(
    film_id: UUID,
    user=Depends(get_current_user),
    bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service),
) -> Response(status_code=status.HTTP_200_OK):
    await bookmark_service.delete_bookmark(user.user_id, film_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/bookmarks/",
    response_model=None,
    summary="Get bookmark",
    description="Get a bookmark",
    response_description="user_id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user."
        },
        status.HTTP_404_NOT_FOUND: {"description:": "bookmarks not found"},
    },
)
async def get_bookmarks(
    user=Depends(get_current_user),
    bookmark_service: BookmarkServiceABC = Depends(get_bookmark_service),
) -> list[ShortBookmark]:
    bookmarks = await bookmark_service.get_bookmarks(user.user_id)
    if not bookmarks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="bookmarks not found"
        )
    return bookmarks
