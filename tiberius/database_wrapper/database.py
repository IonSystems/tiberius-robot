#!/usr/bin/python
import abc


class Database:
    '''
    An abstract Database class.
    Subclasses of Database can be built for any database engine.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def query(self, table_name, column_name, conditions=None):
        '''
        A wrapper function allowing SQL quries to be generated without
        providing SQL statements directly.

        :param table_name: Name of the table to query.
        :param column_name: The column name to return in the result
            of the query.
            Set to None to return all columns.
        :param conditions: A dictionary giving conditions for the query.
        :return: A dictionary containing the results of the query.

        :Example:

        >>> import tiberius.database_wrapper.polyhedra_database as pd
        >>> a = pd.PolyhedraDatabase("test_instance")
        >>> a.sql("CREATE TABLE test_table (id int primary key, test_column varchar(1));")
        >>> a.sql("INSERT INTO test_table (0, 'a');")
        >>> a.query("test_table","test_column")
        [('a', )]
        >>> a.query("test_table","*")
        [(0, 'a')]
        '''
        pass

    @abc.abstractmethod
    def insert(self, table_name, values):
        '''
        A wrapper function allowing SQL insert statements to be generated
        without providing SQL statements directly.

        :param table_name: The table to insert into.
        :param values: .
        :return: A dictionary containing the results of the query.
        '''
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
