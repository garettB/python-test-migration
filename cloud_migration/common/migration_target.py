from .cloud_type import CloudType
from .credentials import Credentials
from .workload import Workload

from ..persistence.persistable import Persistable


class MigrationTarget(Persistable):
    def __init__(self, cloud_type: CloudType, cloud_credentials: Credentials, target_vm: Workload):
        self.cloud_type = cloud_type
        self.cloud_credentials = cloud_credentials
        self.target_vm = target_vm

    @property
    def cloud_type(self):
        return self._cloud_type

    @cloud_type.setter
    def cloud_type(self, new_cloud_type: CloudType):
        if not isinstance(new_cloud_type, CloudType):
            raise ValueError(f"Invalid value for `cloud_type`, {new_cloud_type}, must be of type CloudType")
        self._cloud_type = new_cloud_type
