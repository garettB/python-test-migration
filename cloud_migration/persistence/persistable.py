try:
    import cPickle as pickle
except ImportError:
    import pickle

import logging
import os


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class Persistable():
    def save(self, file_path: str = ''):
        if file_path and not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = os.path.join(file_path, self.__class__.__name__)
        with open(file_name, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_path: str = '') -> object:
        file_name = os.path.join(file_path, cls.__name__)
        if not os.path.exists(file_name):
            LOGGER.error(f"Error loading file, specified file does not exist: {file_name}")
            return None
        with open(file_name, "rb") as f:
            return pickle.load(f)

    @classmethod
    def clear(cls, file_path: str = '') -> bool:
        file_name = os.path.join(file_path, cls.__name__)
        if not os.path.exists(file_name):
            LOGGER.error(f"Error clearing file, specified file does not exist: {file_name}")
            return False
        os.remove(file_name)
        return True
