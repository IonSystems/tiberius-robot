Tiberius's In-Memory Database
=============================

Introduction
------------
Tiberius's in-memory database modules provides a consistent interface with different database engines.
The most integrated engine is Polyhedra, followed by SQLite.

Our repository contains two important database modules:
- `database_wrapper`: Wrapper classes for Polyhedra and SQLite, agnostic to Tiberius so the module can be used for any project.
- `database`: Tiberius-specific definitions. Python-defined schemas, queries, insert functions.

We use these two modules together to provide an easy to use set of functions, for simple integration to other Python software.

Installation
------------
Installation of the database package is included in the setup script.
It takes care of the following:
- Install Python ODBC
- Install Polyhedra Lite Executables and Driver
- Configure ODBC data source for Polyhedra
- Install Unix ODBC

Starting the rtrdb database server
----------------------------------

RTRDB is Polyhedra's database server, and must be running if you want to use the database.
To start the server run:

.. code-block:: none

  rtrdb -r data_service=8001 -r verbosity=4 db

You can add an ampersand at the end of the command if you want to detach it from the terminal and run it in the background:

.. code-block:: none

  sqlc -r data_service=8001 -r verbosity=4 db &

.. note::

  `rtrdb` must be in the `$PATH` environment variable.
  Otherwise you'll need to provide the full path.
  Our installation process should add the full path to `$PATH` already,
  but if that fails you can manually add the path:

    .. code-block:: none

      export PATH=/home/pi/poly9.0/linux/raspi/bin/:$PATH


Using pyodbc with Polyhedra
---------------------------

When using pyodbc with Polyhedra you must make sure autocommit is enabled,
otherwise you won't have much luck getting it to work.
And yes, we found that out the hard way
(See https://sites.google.com/site/polyhedradownloadsite/manuals/odbc-api, bottom of page 184).

This is how we do it:

.. code-block:: none

  self.conn = pyodbc.connect('DSN=8001', autocommit=True)

Tiberius's Database Wrapper
---------------------------

To ease integration of the database with existing modules, a set of wrapper classes were created
The database module currently supports the following SQL features:
- INSERT
- DELETE
- DROP
- UPDATE
- SELECT

These SQL features are hidden behind the scenes in our wrapper classes,
to give a consistent interface for multiple database technologies.

This allows developers with little experience in SQL databases to interact with a database easily.

.. note::
  Adding additional functionality to the wrapper will require some knowledge of SQL.

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
