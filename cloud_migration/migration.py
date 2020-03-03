from typing import List
from enum import Enum
from time import time, sleep

from .common.mount_point import MountPoint
from .common.workload import Workload
from .common.migration_target import MigrationTarget

from .persistence.persistable import Persistable


class MigrationState(Enum):
    not_started = 1
    running = 2
    error = 3
    success = 4


class MigrationError(RuntimeError):
    pass


class Migration(Persistable):

    __mock_wait_minutes__ = 3

    def __init__(self, selected_mount_points: List[MountPoint], source: Workload, target: MigrationTarget):
        self._state = MigrationState.not_started
        self.selected_mount_points = selected_mount_points
        self.source = source
        self.target = target

    def run(self):
        self._prevalidate_migration()
        self._state = MigrationState.running

        migration_count = len(self.selected_mount_points)
        total_data_transfer = sum([mount_point.size for mount_point in self.selected_mount_points])
        duration = self.__mock_wait_minutes__ * 60  # 3 minutes
        start_time = time()
        animation = "|/-\\"
        idx = 0

        for index in range(len(self.selected_mount_points)):
            transfer = self.selected_mount_points[index]

            transfer_time = (transfer.size / total_data_transfer) * duration
            while time() < (start_time + transfer_time):
                job_percent = int(((time() - start_time) / transfer_time) * 100)
                print(f"  {index+1}/{migration_count}\t{transfer.name} {transfer.size} to {self.target.cloud_type.name}\t{job_percent}% {animation[idx % len(animation)]}", end="\r")
                sleep(0.1)
                idx += 1
            self.target.target_vm.storage.append(self.selected_mount_points[index])
        self._state = MigrationState.success

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, _):
        raise AttributeError("Attribute `state` is read-only")

    def _prevalidate_migration(self):
        if self._state == MigrationState.success:
            raise MigrationError("Migration already completed")

        if 'C:\\' not in [mount_point.name for mount_point in self.selected_mount_points]:
            self._state = MigrationState.error
            raise MigrationError(f"Migration cannot proceed if `C:\\` is not available as a source")

        for mount_point in self.selected_mount_points:
            if mount_point not in self.source.storage:
                self._state = MigrationState.error
                raise MigrationError(f"Selected mount point `{mount_point.name}` is not available for migration")
