import sys
from tiberius.database.sqlite_database import SqliteDatabase
from tiberius.utils import detection

'''**********************************************************
    Added functions to provide 'mock' data to the bus
**********************************************************'''
if detection.detect_windows():
    db = SqliteDatabase('D:\\tiberius\smbus_database.db')
else:
    db = SqliteDatabase('/etc/tiberius/smbus_database.db')
tn = "smbus_data"


def initialise_database():
    try:
        db.drop(tn)
    except SqliteDatabase.OperationalError as e:
        print e.value
    db.create(tn, {'address': 'int', 'register': 'int', 'value': 'int'})
    # for address in range(0x00, 0xFF):
    #     for register in range(0x00, 0xFF):
    #         db.insert(tn, {'address': address, 'value': 0, 'register': 0})


def get_value(device_address, register_address):
    return db.query(tn, "value", {
        'clause': 'WHERE',
        'logic': 'AND',
        'data': [
            {
                'column': 'address',
                'assertion': '=',
                'value': device_address
            },
            {
                'column': 'register',
                'assertion': '=',
                'value': register_address
            }
        ]
    })[0][0]


def set_value(device_address, register_address, value):
    db.insert(tn, {'value': value, 'address': device_address,
                   'register': register_address})

if __name__ == "__main__":
    initialise_database()
    #set_value(0x23, 0x43, 100)
    # print get_value(0x23, 0x43)
