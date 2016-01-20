import unittest
import time
import os
import sys
import random
import subprocess
import sqlite3
# TODO: rename module or something
sys.path.insert(0, '../database')
from sqlite_database import SqliteDatabase


def clean_up():
    p = subprocess.Popen(
        'find . -type f -name "test_db_*" -exec rm -f {} \;', shell=True)

# clean_up()
sql = SqliteDatabase("test_db_" + str(random.randint(1, 1000000)) + '.db')
'''
	Ensures that the database implementations are error-free.
'''


class CreateTestDatabase(unittest.TestCase):
    '''Create a databse table for running the following tests on'''

    def runTest(self):
        try:
            self.assertRaises(SqliteDatabase.OperationalError,
                              sql.drop("test_table"))
        except SqliteDatabase.OperationalError as e:
            print e.value
        sql.create("test_table", {'test_column': 'int', 'test_column2': 'int'})


class InsertDatabase(unittest.TestCase):

    def runTest(self):
        sql.insert("test_table", {'test_column': '100',
                                  'test_column2': 'This is a test'})


class GenerateQueryString(unittest.TestCase):

    def runTest(self):
        specimen = sql._SqliteDatabase__generate_insert(
            "insert", "test_table", {'test_column': '100', 'test_column2': 'This is a test'})
        control = "INSERT INTO test_table (test_column, test_column2) VALUES (100, 'This is a test')"
        self.assertEquals(specimen, control)

        specimen = sql._SqliteDatabase__generate_insert(
            "insert or replace", "test_table", {'test_column': '100', 'test_column2': 200})
        control = "INSERT OR REPLACE INTO test_table (test_column, test_column2) VALUES (100, 200)"
        self.assertEquals(specimen, control)


class GenerateQueryConditions(unittest.TestCase):

    def runTest(self):
        specimen = sql._SqliteDatabase__generate_conditions(
            {
                'clause': 'WHERE',
                'logic': "AND",
                'data': [
                    {
                        'column': 'test_column',
                        'assertion': '=',
                        'value': 32
                    },
                    {
                        'column': 'test_column2',
                        'assertion': '=',
                        'value': "Cameron"
                    }
                ]
            })
        control = "WHERE test_column = 32 AND test_column2 = 'Cameron'"
        self.assertEquals(specimen, control)

        specimen = sql._SqliteDatabase__generate_conditions(
            {
                'clause': 'WHERE',
                'logic': "OR",
                'data': [
                    {
                        'column': 'test_column',
                        'assertion': '=',
                        'value': 'hello'
                    },
                    {
                        'column': 'test_column2',
                        'assertion': '>',
                        'value': 54
                    }
                ]
            })
        control = "WHERE test_column = 'hello' OR test_column2 > 54"
        self.assertEquals(specimen, control)


class GenerateDeleteQuery(unittest.TestCase):

    def runTest(self):
        specimen = sql._SqliteDatabase__generate_delete("test_table", {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'test_column',
                    'assertion': '=',
                    'value': 32
                }
            ]
        })
        control = "DELETE FROM test_table WHERE test_column = 32"
        self.assertEquals(specimen, control)

        specimen = sql._SqliteDatabase__generate_delete("test_table", {
            'clause': 'WHERE',
            'logic': "AND",
            'data': [
                {
                    'column': 'test_column',
                    'assertion': '=',
                    'value': 32
                },
                {
                    'column': 'test_column2',
                    'assertion': '=',
                    'value': "Cameron"
                }
            ]
        })
        control = "DELETE FROM test_table WHERE test_column = 32 AND test_column2 = 'Cameron'"
        self.assertEquals(specimen, control)


class DeleteAllFromTableDatabase(unittest.TestCase):

    def runTest(self):
        try:
            sql.create("test_table", {
                       'test_column': 'int', 'test_column2': 'int'})
        except sqlite3.OperationalError:
            print ""
        sql.delete("test_table")


class GenerateUpdateQuery(unittest.TestCase):

    def runTest(self):
        specimen = sql._SqliteDatabase__generate_update("test_table",
                                                        {
                                                            'ContactName': 'Alfred Schmidt',
                                                            'City': 'Hamburg'
                                                        },
                                                        {
                                                            'clause': 'WHERE',
                                                            'data': [
                                                                {
                                                                    'column': 'CustomerName',
                                                                    'assertion': '=',
                                                                    'value': 'Alfreds Futterkiste'
                                                                }
                                                            ]
                                                        })
        control = "UPDATE test_table SET ContactName='Alfred Schmidt', City='Hamburg' WHERE CustomerName = 'Alfreds Futterkiste'"
        specimen = specimen.replace(',', '')
        control = control.replace(',', '')
        self.assertItemsEqual(specimen.split(' '), control.split(' '))


class GenerateSelectQuery(unittest.TestCase):

    def runTest(self):
        specimen = sql._SqliteDatabase__generate_query(
            "select", 'test_table', "*", None)
        control = "SELECT * FROM test_table"
        self.assertEquals(specimen, control)

        specimen = sql._SqliteDatabase__generate_query(
            "select", "test_table", 'test_column', None)
        control = "SELECT test_column FROM test_table"
        self.assertEquals(specimen, control)

        specimen = sql._SqliteDatabase__generate_query("select", "test_table", 'test_column',
                                                       {
                                                           'clause': 'WHERE',
                                                           'data': [
                                                               {
                                                                   'column': 'CustomerName',
                                                                   'assertion': '=',
                                                                   'value': 'Alfreds Futterkiste'
                                                               }
                                                           ]
                                                       })
        control = "SELECT test_column FROM test_table WHERE CustomerName = 'Alfreds Futterkiste'"
        self.assertEquals(specimen, control)


class QueryDatabase(unittest.TestCase):

    def runTest(self):
        try:
            sql.create("test_table", {
                       'test_column': 'int', 'test_column2': 'int'})
        except sqlite3.OperationalError:
            print ''
        sql.insert("test_table", {'test_column': 99, 'test_column2': 20})
        sql.query("test_table", "*")

        # Last test cleans up
        clean_up()

if __name__ == "__main__":
    q = GenerateSelectQuery()
    q.runTest()
