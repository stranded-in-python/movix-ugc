from .abc import StorageABC


class LikeStorage(StorageABC):

    def __init__(self, storage):
        self.storage 