from ..persistence.persistable import Persistable


class Credentials(Persistable):
    def __init__(self, username: str, password: str, domain: str):
        self.username = username
        self.password = password
        self.domain = domain
