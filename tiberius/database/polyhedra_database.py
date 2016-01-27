import abc
from database import Database
from clauses import SqlClauses
import subprocess
import pyodbc

class PolyhedraDatabase(Database):

    def __init__(self, name):
        # Start the database API
        popen = subprocess.Popen("rtrdb -r data_service=8001 -r verbosity=4 db", shell = True, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, b"")
        for line in lines_iterator:
            if line == "Ready":
                break
            if "Failed" in line:
                break
        # The database, defined by its location
        self.conn = pyodbc.connect('DSN=8001', autocommit=True)

        # This is the cursor that is used to execute SQL commands.
        self.c = self.conn.cursor()

    def test(self):
        #self.c.execute("CREATE TABLE test_table2 (column1 int primary key, column2 text)")
        #self.conn.commit()
	result = 0
        self.c.execute("SELECT id,column from test_table")
	print self.c.fetchall()
        self.c.execute("INSERT INTO test_table (id, column) VALUES (0, 33)")
	self.c.commit()
        self.c.execute("SELECT id,column from test_table")
        print self.c.fetchall()
        #self.conn.commit()
        
    '''*******************************************************************
        Accessible functions, according to Abstract Base Class (Database)
    *******************************************************************'''

    def query(self, table_name, column_name, conditions=None):
        query = self.__generate_query(
            SqlClauses.SELECT.value, table_name, column_name, conditions)
        self.c.execute(query)
        return self.c.fetchall()

    def insert(self, table_name, values):
        query = self.__generate_insert("insert", table_name, values)
        try:
            self.c.execute(query)
            self.conn.commit()
        except pyodbc.OperationalError as e:
            raise PolyhedraDatabase.OperationalError(e[0])

    def drop(self, table_name):
        try:
            self.c.execute(self.__generate_drop(table_name))
            self.conn.commit()
        except pyodbc.OperationalError as e:
            raise PolyhedraDatabase.OperationalError(e[0])
    '''
        Example operation:
        update("Customers",
            {
                'ContactName': 'Alfred Schmidt',
                'City': 'Hamburg'
            },
            {
                'clause':'WHERE',
                'data': [
                    {
                        'column' : 'CustomerName',
                        'assertion' : '=',
                        'value': 'Alfreds Futterkiste'
                    }
                ]
            })

        Should result in:
        UPDATE Customers
        SET ContactName='Alfred Schmidt', City='Hamburg'
        WHERE CustomerName='Alfreds Futterkiste';
    '''

    def update(self, table_name, data, conditions):
        query = self.__generate_update(table_name, data, conditions)
        self.c.execute(query)
        self.conn.commit()
        return

    def delete(self, table_name, conditions=None):
        statement = self.__generate_delete(table_name, conditions)
        self.c.execute(statement)
        self.conn.commit()
        return

    def create(self, table_name, columns):
        query = self.__generate_create(table_name, columns)
        print query
        try:
            self.c.execute(query)
            # Set database properties
            self.c.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except pyodbc.OperationalError as e:
            raise PolyhedraDatabase.OperationalError(e)

    '''*******************************************************************
        Hidden functions
    *******************************************************************'''

    def __generate_update(self, table_name, data, conditions):
        query = ""
        query += SqlClauses.UPDATE.value + " "
        query += table_name + " "
        query += SqlClauses.SET.value + " "
        for c_name, c_value in data.iteritems():
            query += c_name
            query += '='
            query += self.__generate_representation(c_value)
            query += ", "
        query = query[:-2]  # Remove last comma
        query += " "
        query += self.__generate_conditions(conditions)
        return query

    def __generate_drop(self, table_name):
        query = SqlClauses.DROP_TABLE.value + " "
        query += table_name
        return query

    def __generate_insert(self, t, table_name, values):
        query = ""
        if "insert" in t:
            query += SqlClauses.INSERT.value + " "
        if "or" in t:
            query += SqlClauses.OR.value + " "
        if "replace" in t:
            query += SqlClauses.REPLACE.value + " "
        query += SqlClauses.INTO.value + " "

        query += table_name
        query += " ("
        for c_name, value in values.iteritems():
            q = ""
            q += c_name + ", "
            query += q
        query = query[:-2]
        query += ") " + SqlClauses.VALUES.value + " ("
        for c_name, value in values.iteritems():
            q = ""
            q += self.__generate_representation(value) + ", "
            query += q
        query = query[:-2]
        query += ")"
        return query

    def __generate_delete(self, table_name, conditions):
        query = SqlClauses.DELETE.value + " "
        query += SqlClauses.FROM.value + " "
        query += table_name
        if not conditions:
            return query
        else:
            query += " " + self.__generate_conditions(conditions)
            return query

    def __generate_query(
            self,
            query_type,
            table_name,
            column_name,
            conditions):
        query = ""
        if query_type.upper() == SqlClauses.SELECT.value:
            query += SqlClauses.SELECT.value + " "
        query += column_name + " "
        query += SqlClauses.FROM.value + " "
        query += table_name
        if conditions:
            query += " " + self.__generate_conditions(conditions)
        return query

    def __generate_conditions(self, conditions=None):
        cond_str = ""
        if conditions:
            cond_str = conditions['clause'] + " "
            if 'logic' in conditions:
                logic = conditions['logic']
            else:
                logic = ""
            for condition in conditions['data']:
                c_str = ""
                c_str += condition['column'] + " "
                c_str += condition['assertion'] + " "
                c_str += self.__generate_representation(
                    condition['value']) + " "
                c_str += logic + " "
                cond_str += c_str
            cond_str = cond_str[:-(len(logic) + 2)]
            return cond_str
        else:
            return ""

    def __generate_representation(self, value):
        try:
            int(value)
            return str(value)
        except:
            return "'" + value + "'"

    def __generate_create(self, table_name, columns):
        query = ""
        query += SqlClauses.CREATE_TABLE.value + " "
        query += table_name
        query += " " + self.__generate_columns(columns)
        return query

    def __generate_columns(self, columns):
        query = "("
        for c_name, c_type in columns.iteritems():
            query += c_name + " " + c_type + ", "
        query = query[:-2]  # Remove the last comma
        query += ")"
        return query

#For testing
if __name__ == "__main__":
    p = PolyhedraDatabase('tiberius-polyhedra')
    #p.create('test_table', {'column1' : 'int', 'column2': 'int'})
    p.test()
