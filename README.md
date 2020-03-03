# Python Test Migration

This package simulates the migration of various mount points to a specified cloud instance. Once initiated the `migration` will simulate the data transfer, providing a progress output to the console.

## Requirements

This package requires Python version 3.6 or higher to operate and `pip`, a Python package manager, to install. Instructions for installing `pip` can be found [here](https://pip.pypa.io/en/stable/installing/).

## Installation

Install using `pip`

```
pip install <my_package>
```

## Test Cases

Basic and migration-operation test cases have been created and can be run using the following `pip` command which will install the package if the tests pass or display an error if they fail.

```
pip install <my_package> --install-option test
```
---

## Usage

This package is installed using a module named `cloud_migration` with the following class structure:

### common

Contains common components used for setting up the migration.

#### cloud_type

Contains an enumeration class, `CloudType`, listing the only supported cloud options for the migration target.

```python
from cloud_migration.common.cloud_type import CloudType

cloud_type = CloudType.aws
```

#### credentials

The `Credentials` class is used to specify credentials (username, password, domain) for use with both `Workload` and `MigrationTarget` classes.

```python
from cloud_migration.common.credentials import Credentials

credentials = Credentials(username='username', password='password', domain='domain.com')
```

#### migration_target

The `MigrationTarget` class defines the target for data migrations (where data will be transferred to).

```python
...
from cloud_migration.common.migration_target import MigrationTarget

cloud_ip_address = "179.122.4.77"
cloud_credentials = Credentials(username='cloud_username', password='cloud_password', domain='cloud_domain.com')
workload_target = Workload(ip=cloud_ip_address, credentials=cloud_credentials)
cloud_type = CloudType.aws

migration_target = MigrationTarget(cloud_type=cloud_type, cloud_credentials=cloud_credentials, target_vm=workload_target)
```

#### mount_point

The `MountPoint` class defines a generic mount point that includes a name (e.g. 'C:\') and a size.
```python
from cloud_migration.common.mount_point import MountPoint

mount_point = MountPoint(name="D:\\", size=750)
```

#### workload

The `Workload` class holds a list of `MountPoint`s as well as an IP address and `Credentials`.

```python
...
from cloud_migration.common.workload import Workload

ip_address = "10.10.24.33"
credentials = Credentials(username='username', password='password', domain='domain.com')
mount_points = [
    MountPoint(name="D:\\", size=750)
]

workload = Workload(ip=ip_address, credentials=credentials, storage=mount_points)
```

NOTE: For a single session no `Workload` may contain the same IP address value as another `Workload`, and the IP address is read-only

NOTE: For the `Credentials`, neither the `username` or `password` can be `None`

### persistence

All classes defined inherit from `persistence.Persistable` allowing them to be saved to the file system, using Python's `pickle` module. `Persistable` supports 3 different operations:
#### Save

The `save()` operation will save a representation of the class to the file system in the current directory. Optionally you can use the `file_path` parameter to choose the directory.

```python
workload.save(file_path='customer1')
```

#### Load

The `load()` operation is a class method which takes an optional `file_path` paremeter or defaults to the current working directory. This will return a representation of the specified class' object if successful, or `None` if not.

```python
workload = Workload.load(file_path='customer1')
```

#### Clear

The `clear()` operation is a class method which also takes an optional `file_path` paremeter or defaults to the current working directory. This operation will return `True` if successful, `False` if not.

```python
is_successful = Workload.clear(file_path='customer1')
```


### migration

The business logic of the transfer takes place in the `Migration` class, which takes the following parameters:
1. List of selected `MountPoint`s desired to be migrated to the target VM, these must be a subset of the source `Workload` `MountPoint`s and must include a `MountPoint` with name `C:\`
1. A source `Workload` which includes a list of source `MountPoint`s that are able to be selected as well as values necessary to access those `MountPoint`s.
1. A `MigrationTarget`, where the selected `MountPoint`s from the source `Workload` will be migrated.

Once the class is configured, executing the migration is performed using the `Migration#run()` command.

```python
...
from cloud_migration.migration import Migration
from cloud_migration.migration import MigrationError

migration = Migration(selected_mount_points=selected_mount_points, source=workload_source, target=migration_target)
try:
    migration.run()
except MigrationError as error:
    LOGGER.error(error)
LOGGER.warning(f"Migration completed with a status of: {migration.state.name}")
```

NOTE: Should any error arise during the migration it is expected that a `MigrationError` will be raised. The expected end state of the `run()` that the `Migration#state` will be `MigrationState.success`; if an error is raised then it is expected that the `state` will instead be `MigrationState.error`.


## Example

Below is a basic but complete example of a migration:

```python
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

```