# Database
Contains database interaction functions that are specific to Tiberius. See the `database` module if you are interested in a non-specific Polyhedra database wrapper.

# Developers
Please use this module to define:
- database table definitions, creations
- database queries
- any special decorators related to the database, such as the ones already present.

# Files

## `create.py`
Contains functions to create table in the Polyhedra database.

## `decorators.py`
These decorators are used to insert into the database on-the-go, as actuators are instructed to move.

## `query.py`
Contains query functions for getting data from the database.

## 'tables.py'
Defines the table names and columns for each table used by Tiberius.
