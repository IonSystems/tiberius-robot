from enum import Enum

class SqlClauses(Enum):
    WHERE = "WHERE"
    SELECT = "SELECT"
    FROM = "FROM"
    CREATE_TABLE = "CREATE TABLE"
    INSERT = "INSERT"
    OR = "OR"
    REPLACE = "REPLACE"
    INTO = "INTO"
    VALUES = "VALUES"
    DELETE = "DELETE"
    DROP_TABLE = "DROP TABLE"
    UPDATE = "UPDATE"
    SET = "SET"
