#!/usr/bin/python
import abc
import sqlite3
from database import Database
from clauses import SqlClauses


class SqliteDatabase(Database):

    def __init__(self, name):
        # The database, defined by its location
        self.conn = sqlite3.connect(name)
        # This is the cursor that is used to execute SQL commands.
        self.c = self.conn.cursor()

    '''*******************************************************************
        Accessible functions, according to Abstract Base Class (Database)
    *******************************************************************'''

    def set_db_name(self, name):
        self.conn = sqlite3.connect(name)
        self.c = self.conn.cursor()

    def query(self, table_name, column_name, conditions=None):
        query = self.__generate_query(
            SqlClauses.SELECT, table_name, column_name, conditions)
        self.c.execute(query)
        return self.c.fetchall()

    def insert(self, table_name, values):
        query = self.__generate_insert("insert", table_name, values)
        try:
            self.c.execute(query)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise SqliteDatabase.OperationalError(e[0])

    def drop(self, table_name):
        try:
            self.c.execute(self.__generate_drop(table_name))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise SqliteDatabase.OperationalError(e[0])
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
        try:
            self.c.execute(query)
            # Set database properties
            self.c.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise SqliteDatabase.OperationalError(e)

    '''*******************************************************************
        Hidden functions
    *******************************************************************'''

    def __generate_update(self, table_name, data, conditions):
        query = ""
        query += SqlClauses.UPDATE + " "
        query += table_name + " "
        query += SqlClauses.SET + " "
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
        query = SqlClauses.DROP_TABLE + " "
        query += table_name
        return query

    def __generate_insert(self, t, table_name, values):
        query = ""
        if "insert" in t:
            query += SqlClauses.INSERT + " "
        if "or" in t:
            query += SqlClauses.OR + " "
        if "replace" in t:
            query += SqlClauses.REPLACE + " "
        query += SqlClauses.INTO + " "

        query += table_name
        query += " ("
        for c_name, value in values.iteritems():
            q = ""
            q += c_name + ", "
            query += q
        query = query[:-2]
        query += ") " + SqlClauses.VALUES + " ("
        for c_name, value in values.iteritems():
            q = ""
            q += self.__generate_representation(value) + ", "
            query += q
        query = query[:-2]
        query += ")"
        return query

    def __generate_delete(self, table_name, conditions):
        query = SqlClauses.DELETE + " "
        query += SqlClauses.FROM + " "
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
        if query_type.upper() == SqlClauses.SELECT:
            query += SqlClauses.SELECT + " "
        query += column_name + " "
        query += SqlClauses.FROM + " "
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
        query += SqlClauses.CREATE_TABLE + " "
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
