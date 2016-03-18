import unittest
import time
import os
import sys
import random
import subprocess
import sqlite3
from tiberius.database.sqlite_database import SqliteDatabase

def clean_up():
    p = subprocess.Popen(
        'find . -type f -name "test_db_*" -exec rm -f {} \;', shell=True)

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

        # Create a table in our database called 'test_table', with two columns
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

class DeleteAllFromTableDatabase(unittest.TestCase):

    def runTest(self):
        with self.assertRaises(SqliteDatabase.OperationalError):
            sql.create("test_table", {'test_column': 'int', 'test_column2': 'int'})

        sql.delete("test_table")

        # Make sure there is nothing left in the table
        results = sql.query("test_table", "*")
        self.assertEquals(results, [])

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

class DropTable(unittest.TestCase):
    def runTest(self):
        sql.create("drop_table", {
                   'test_column': 'int', 'test_column2': 'int'})

        sql.drop("drop_table")

        # Ensure that an operational error is raised when we try to drop the table again.
        with self.assertRaises(SqliteDatabase.OperationalError):
            sql.drop("drop_table")

class QueryDatabase(unittest.TestCase):

    def runTest(self):
        sql.create("query_table", {
                   'test_column': 'int', 'test_column2': 'int'})

        # Ensure sql.query() returns all columns
        sql.insert("query_table", {'test_column': 99, 'test_column2': 20})
        results = sql.query("query_table", "*")
        self.assertEquals(results, [(99, 20)])

        # Ensure sql.query() returns all rows
        sql.insert("query_table", {'test_column': 33, 'test_column2': 66})
        results = sql.query("query_table", "*")
        self.assertEquals(results, [(99, 20), (33, 66)])

        # Ensure sql.query() returns correct column
        sql.insert("query_table", {'test_column': 434, 'test_column2': 3423})
        results = sql.query("query_table", "test_column")
        self.assertEquals(results, [(99,), (33,), (434,)])

        # Last test cleans up
        clean_up()

if __name__ == "__main__":
    unittest.main()
