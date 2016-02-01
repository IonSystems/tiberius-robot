import unittest
import time
import os
import sys
import random
import subprocess
from tiberius.database.polyhedra_database import PolyhedraDatabase


def clean_up():
    p = subprocess.Popen(
        'find . -type f -name "test_db_*" -exec rm -f {} \;', shell=True)

pol = PolyhedraDatabase("test_db_" + str(random.randint(1, 1000000)) + '.db')


class CreateTestDatabase(unittest.TestCase):
    '''Create a database table for running the following tests on'''

    def runTest(self):
        try:
            self.assertRaises(PolyhedraDatabase.OperationalError,
                              pol.drop("test_table"))
        except PolyhedraDatabase.OperationalError as e:
            print e.value

        # Create a table in our database called 'test_table', with two columns
        pol.create("test_table",
                   {'test_column': 'int primary key',
                    'test_column2': 'int'})


class InsertDatabase(unittest.TestCase):

    def runTest(self):
        pol.insert("test_table", {'test_column': '100',
                                  'test_column2': 2})


class GenerateQueryString(unittest.TestCase):

    def runTest(self):
        specimen = pol._PolyhedraDatabase__generate_insert(
            "insert", "test_table",
            {'test_column': '100',
             'test_column2': 'This is a test'})
        control = "INSERT INTO test_table (test_column, test_column2) " \
        "VALUES (100, 'This is a test')"
        self.assertEquals(specimen, control)

        specimen = pol._PolyhedraDatabase__generate_insert(
            "insert or replace",
            "test_table",
            {'test_column': '100', 'test_column2': 200})
        control = "INSERT OR REPLACE INTO test_table " \
        "(test_column, test_column2) VALUES (100, 200)"
        self.assertEquals(specimen, control)


class GenerateQueryConditions(unittest.TestCase):

    def runTest(self):
        specimen = pol._PolyhedraDatabase__generate_conditions(
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

        specimen = pol._PolyhedraDatabase__generate_conditions(
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
        with self.assertRaises(PolyhedraDatabase.TableAlreadyExistsError):
            pol.create("test_table3", {
                       'test_column': 'int primary key',
                       'test_column2': 'int'})

        pol.delete("test_table3")

        # Make sure there is nothing left in the table
        results = pol.query("test_table3", "*")
        self.assertEquals(results, [])


class GenerateSelectQuery(unittest.TestCase):

    def runTest(self):
        specimen = pol._PolyhedraDatabase__generate_query(
            "select", 'test_table', "*", None)
        control = "SELECT * FROM test_table"
        self.assertEquals(specimen, control)

        specimen = pol._PolyhedraDatabase__generate_query(
            "select", "test_table", 'test_column', None)
        control = "SELECT test_column FROM test_table"
        self.assertEquals(specimen, control)

        specimen = pol._PolyhedraDatabase__generate_query(
         "select", "test_table", 'test_column',
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
        control = "SELECT test_column FROM test_table " \
        "WHERE CustomerName = 'Alfreds Futterkiste'"
        self.assertEquals(specimen, control)


class DropTable(unittest.TestCase):

    def runTest(self):
        pol.create("drop_table", {
                   'test_column': 'int primary key', 'test_column2': 'int'})

        pol.drop("drop_table")

        # Ensure that an operational error is raised when we try to drop the
        # table again.
        with self.assertRaises(PolyhedraDatabase.NoSuchTableError):
            pol.drop("drop_table")


class TestCreateInsertDeleteDrop(unittest.TestCase):

    def runTest(self):
	table_name = "test_table2"
        p = PolyhedraDatabase('tiberius-polyhedra')
        try:
            p.create(table_name, {'id': 'int primary key', 'column': 'int'})
        except PolyhedraDatabase.TableAlreadyExistsError as e:
            print "Table already exists"
        p.insert(table_name, {'id': '0', 'column': '0'})
        p.insert(table_name, {'id': '1', 'column': '2'})
        p.insert(table_name, {'id': '2', 'column': '4'})
        p.insert(table_name, {'id': '3', 'column': '6'})
        p.insert(table_name, {'id': '4', 'column': '8'})
        # TODO: Validate output
	p.query(table_name, '*')
        p.drop(table_name)

        p.create('complex_table', {'id': 'int primary key',
                                   'name': 'varchar(50)',
                                   'address': 'varchar(200)',
                                   'robot_id': 'int'})
        p.insert('complex_table', {'id': '0',
                                   'name': 'Cameron A. Craig',
                                   'address': '1979 Hannover Street',
                                   'robot_id': 0})
	#TODO: Validate output
        p.query('complex_table', '*')
        p.delete('complex_table')
        p.query('complex_table', '*')
        p.drop('complex_table')


class QueryDatabase(unittest.TestCase):

    def runTest(self):
       	pol.create("query_table", {
                   'test_column': 'int primary key', 'test_column2': 'int'})

        # Ensure pol.query() returns all columns
        pol.insert("query_table", {'test_column': 99, 'test_column2': 20})
        results = pol.query("query_table", "*")
        self.assertItemsEqual((99, 20), results[0])

        # Ensure pol.query() returns all rows
        pol.insert("query_table", {'test_column': 33, 'test_column2': 66})
        results = pol.query("query_table", "*")
        self.assertItemsEqual(results[0], (99, 20))
        self.assertItemsEqual(results[1], (33, 66))
        # Ensure pol.query() returns correct column

        pol.insert("query_table", {'test_column': 434, 'test_column2': 3423})
        results = pol.query("query_table", "*")
        self.assertItemsEqual(results[0], (99, 20))
        self.assertItemsEqual(results[1], (33, 66))
        self.assertItemsEqual(results[2], (434, 3423))

	# Drop the table because we're done with it
	pol.drop("query_table")

        # Last test cleans up
        clean_up()

if __name__ == "__main__":
    unittest.main()
