Tiberius's Database Module
==========================

Introduction
------------
Tiberius's database module provides a consistent interface between your Python programs and a number of database technologies.

Installation
------------
Installation of the database package is included in the setup script.

Tiberius's Database Interface
-----------------------------
The database module currently supports the following SQL features:
- INSERT
- DELETE
- DROP
- UPDATE
- SELECT

These SQL features are hidden behind the scenes in our wrapper classes, to give a consistent interface for multiple database technologies.

Example Usage
~~~~~~~~~~~~~

The following example shows all currently supported database interactions::

    #Create a new Database
    db = PolyhedraDatabase('example_db')

    #Create a table with a few columns.
    db.create('example_table', {'id': 'int primary key', 'example_column':'varchar(100)'})

    #Insert a row into the table
    db.insert('example_table', {'id': 0, 'example_column':'Example text value.'})

    #Query the table for all rows an columns
    results = db.query('example_table', '*')
    print results

    #Update the value we previously put in
    db.update('example_table',
            {
                'example_column': 'Example new updates value.',
            },
            {
                'clause':'WHERE',
                'data': [
                    {
                        'column' : 'id',
                        'assertion' : '=',
                        'value': '0'
                    }
                ]
            })

    #Drop the table
    db.drop('example_table')
