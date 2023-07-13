from uuid import UUID

from .abc import StorageABC


class LikeStorage(StorageABC):

    def __init__(self, manager):
        self.manager = manager

    async def get_by_id(self, film_id: UUID):
        await self.manager.get_by_id(film_id)
