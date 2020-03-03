import unittest
import logging

from common.cloud_type import CloudType
from common.credentials import Credentials
from common.migration_target import MigrationTarget
from common.mount_point import MountPoint
from common.workload import Workload

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.valid_credentials = Credentials(username="username", password="password", domain="test.com")
        self.valid_mount_point_list = [
            MountPoint("C:\\", 100),
            MountPoint("D:\\", 5000)
        ]
        self.valid_ip = "192.168.1.1"

    def tearDown(self):
        Workload._ip_list = []

    # Workload: IP cannot change for the specific workload

    def test_workload_ip_change(self):
        workload = Workload(ip=self.valid_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        with self.assertRaises(TypeError):
            workload.ip = "192.168.1.2"

    # Workload: You cannot have more than one source with the same IP

    def test_workload_ip_already_in_use(self):
        duplicate_ip = "192.168.168.168"
        Workload(ip=duplicate_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        with self.assertRaises(ValueError):
            Workload(ip=duplicate_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)

    # Workload: Username, password, IP should not be None

    def test_workload_credential_empty_username(self):
        credentials = self.valid_credentials
        credentials.username = None
        with self.assertRaises(ValueError):
            Workload(ip=self.valid_ip, credentials=credentials, storage=self.valid_mount_point_list)

    def test_workload_credential_empty_password(self):
        credentials = self.valid_credentials
        credentials.password = None
        with self.assertRaises(ValueError):
            Workload(ip=self.valid_ip, credentials=credentials, storage=self.valid_mount_point_list)

    def test_workload_ip_is_none(self):
        none_ip = None
        with self.assertRaises(ValueError):
            Workload(ip=none_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)

    # MigrationTarget: Cloud Type: aws, azure, vsphere, vcloud - no other types are allowed

    def test_migration_target_invalid_cloud_type(self):
        workload = Workload(ip=self.valid_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        credentials = self.valid_credentials
        invalid_cloud_type = "invalid"

        with self.assertRaises(ValueError):
            MigrationTarget(cloud_type=invalid_cloud_type, cloud_credentials=credentials, target_vm=workload)

    def test_migration_target_valid_cloud_type(self):
        workload = Workload(ip=self.valid_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        credentials = self.valid_credentials
        valid_cloud_type = CloudType.azure
        MigrationTarget(cloud_type=valid_cloud_type, cloud_credentials=credentials, target_vm=workload)

    def test_persistence(self):
        workload = Workload(ip=self.valid_ip, credentials=self.valid_credentials, storage=self.valid_mount_point_list)
        workload.save()

        loaded_workload = Workload.load()
        self.assertEqual(workload.ip, loaded_workload.ip)

        for i in range(len(workload.storage)):
            self.assertEqual(workload.storage[i].name, loaded_workload.storage[i].name)
            self.assertEqual(workload.storage[i].size, loaded_workload.storage[i].size)
        credentials = workload.credentials
        loaded_credentials = loaded_workload.credentials

        self.assertEqual(credentials.username, loaded_credentials.username)
        self.assertEqual(credentials.password, loaded_credentials.password)
        self.assertEqual(credentials.domain, loaded_credentials.domain)
        Workload.clear()
