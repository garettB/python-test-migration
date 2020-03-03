from ..persistence.persistable import Persistable


class MountPoint(Persistable):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
