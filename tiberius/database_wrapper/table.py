#!/usr/bin/python
import abc


class Table:
    __metaclass__ = abc.ABCMeta
    columns = {}
    table_name = ""

    def get_columns(self):
        '''
        Return a dict containing the column names and types.
        This dict can be directly passed into Database.create()
        in order to create a new table in the database.
        '''
        return self.columns
