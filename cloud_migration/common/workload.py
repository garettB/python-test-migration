from typing import List

from .credentials import Credentials
from .mount_point import MountPoint

from ..persistence.persistable import Persistable


class Workload(Persistable):

    _ip_list = []

    def __init__(self, ip: str, credentials: Credentials, storage: List[MountPoint] = []):
        if ip is None:
            raise ValueError("Parameter `ip` cannot be None")
        if ip in Workload._ip_list:
            raise ValueError(f"Provided `ip` already in use: {ip}")
        Workload._ip_list.append(ip)
        self._ip = ip
        self.credentials = credentials
        self.storage = storage

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, _):
        raise TypeError("Attribute `ip` is read-only")

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, new_credentials: Credentials):
        if new_credentials.username is None:
            raise ValueError("Credential `username` cannot be None")
        if new_credentials.password is None:
            raise ValueError("Credential `password` cannot be None")
        self._credentials = new_credentials
