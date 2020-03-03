#!/usr/bin/env python3

import logging

from cloud_migration.migration import Migration
from cloud_migration.migration import MigrationError

from cloud_migration.common.cloud_type import CloudType
from cloud_migration.common.credentials import Credentials
from cloud_migration.common.migration_target import MigrationTarget
from cloud_migration.common.mount_point import MountPoint
from cloud_migration.common.workload import Workload


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

if __name__ == '__main__':
    # Step 1: Configure our source mount points
    mount_points = [
        MountPoint(name="C:\\", size=1000),  # `C:\` is required at a minimum and must be present in the selected_mount_points
        MountPoint(name="D:\\", size=1000),
        MountPoint(name="E:\\", size=1000),
        MountPoint(name="F:\\", size=1000),
    ]

    # Step 2: Create a Workload object which will define how to access the mount_points
    ip_address = "10.10.24.33"
    credentials = Credentials(username='username', password='password', domain='domain.com')
    workload_source = Workload(ip=ip_address, credentials=credentials, storage=mount_points)

    # Step 3: Create a list of mount points that we will be migrating, must be a sub-set of the above-created `mount_points`
    #   and must include `C:\`
    selected_mount_points = [
        mount_points[0],
        mount_points[2]
    ]

    # Step 4: Define the target cloud-based VM where we will be migrating the data
    cloud_ip_address = "179.122.4.77"
    cloud_credentials = Credentials(username='cloud_username', password='cloud_password', domain='cloud_domain.com')

    #   Note, the `storage` parameter is left blank, this will be populated during the migration
    workload_target = Workload(ip=cloud_ip_address, credentials=cloud_credentials)

    cloud_type = CloudType.aws
    migration_target = MigrationTarget(cloud_type=cloud_type, cloud_credentials=cloud_credentials, target_vm=workload_target)

    # Step 5: Run the migration; this will throw a MigrationError if a failure occurs
    migration = Migration(selected_mount_points=selected_mount_points, source=workload_source, target=migration_target)
    try:
        migration.run()
    except MigrationError as error:
        LOGGER.error(error)
    LOGGER.warning(f"Migration completed with a status of: {migration.state.name}")
