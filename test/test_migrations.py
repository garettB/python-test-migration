import unittest
import logging

from migration import Migration
from migration import MigrationError
from migration import MigrationState

from common.cloud_type import CloudType
from common.credentials import Credentials
from common.migration_target import MigrationTarget
from common.mount_point import MountPoint
from common.workload import Workload


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class MigrationTests(unittest.TestCase):

    def setUp(self):
        self.valid_credentials = Credentials(username="username", password="password", domain="test.com")
        self.valid_mount_point_list = [
            MountPoint("C:\\", 100),
            MountPoint("D:\\", 5000)
        ]
        self.valid_ip_1 = "192.168.1.1"
        self.valid_ip_2 = "192.168.1.2"

    def tearDown(self):
        # Clear the workload list of IPs that we use to track for duplicates
        Workload._ip_list = []

    # Basic success test case

    def test_migration_basic(self):
        workload_source = Workload(ip=self.valid_ip_1, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        workload_target = Workload(ip=self.valid_ip_2, credentials=self.valid_credentials, storage=[])
        migration_target = MigrationTarget(cloud_type=CloudType.aws, cloud_credentials=self.valid_credentials, target_vm=workload_target)
        migration = Migration(selected_mount_points=self.valid_mount_point_list, source=workload_source, target=migration_target)
        migration.__mock_wait_minutes__ = 0
        migration.run()
        self.assertEqual(migration.state, MigrationState.success)

    # TargetVM and target should only have mount points that are selected

    def test_migration_target_not_in_source(self):
        workload_source = Workload(ip=self.valid_ip_1, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[1]])
        workload_target = Workload(ip=self.valid_ip_2, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[1]])
        migration_target = MigrationTarget(cloud_type=CloudType.aws, cloud_credentials=self.valid_credentials, target_vm=workload_target)
        migration = Migration(selected_mount_points=[self.valid_mount_point_list[0]], source=workload_source, target=migration_target)

        with self.assertRaises(MigrationError):
            migration.run()
        self.assertEqual(migration.state, MigrationState.error)

    def test_migration_change_state(self):
        workload_source = Workload(ip=self.valid_ip_1, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[0]])
        workload_target = Workload(ip=self.valid_ip_2, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[0]])
        migration_target = MigrationTarget(cloud_type=CloudType.aws, cloud_credentials=self.valid_credentials, target_vm=workload_target)
        migration = Migration(selected_mount_points=self.valid_mount_point_list, source=workload_source, target=migration_target)

        with self.assertRaises(AttributeError):
            migration.state = MigrationState.success

    # Implement business logic to not allow running migrations when volume C:\ is not allowed

    def test_migration_target_c_not_allowed(self):
        workload_source = Workload(ip=self.valid_ip_1, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[1]])
        workload_target = Workload(ip=self.valid_ip_2, credentials=self.valid_credentials, storage=[self.valid_mount_point_list[1]])
        migration_target = MigrationTarget(cloud_type=CloudType.aws, cloud_credentials=self.valid_credentials, target_vm=workload_target)
        migration = Migration(selected_mount_points=[self.valid_mount_point_list[1]], source=workload_source, target=migration_target)

        with self.assertRaises(MigrationError):
            migration.run()
        self.assertEqual(migration.state, MigrationState.error)
