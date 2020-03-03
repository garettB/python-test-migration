import sys

path_src = sys.path[0]

if not path_src.endswith('cloud_migration/'):
    sys.path[0] = '{pth}/cloud_migration/'.format(pth=path_src)
