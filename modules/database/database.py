import abc
'''
    An abstract Database, can be implemented for any database.
'''
class Database:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def query(self):
        return

    @abc.abstractmethod
    def insert(self):
        return

    @abc.abstractmethod
    def update(self):
        return

    @abc.abstractmethod
    def delete(self):
        return

    class OperationalError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
