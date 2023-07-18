from datetime import datetime
from uuid import UUID


from .mixins import FilmIDMixin, ReviewIDMixin

class Review(FilmIDMixin, ReviewIDMixin):
    user_id: UUID
    text: str
    timestamp: datetime
    score: int
    likes: int
    dislikes: int


class ReviewLikes(ReviewIDMixin):
    user_id: UUID
    score: int # либо 0, либо 10
