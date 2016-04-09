#!/usr/bin/python
import abc


class Database:
    '''
    An abstract Database, can be implemented for any database.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def query(self):
        pass

    @abc.abstractmethod
    def insert(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    @abc.abstractmethod
    def create(self, table_name, columns):
        pass

    @abc.abstractmethod
    def drop(self, table_name):
        pass

    class OperationalError(Exception):

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class DuplicateKeyError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class NoSuchTableError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class UnknownError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class TableAlreadyExistsError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)
