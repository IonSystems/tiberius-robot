import sqlite3
from colorama import init, Fore
init()

class Settings:

    # This module can be used on each Raspberry Pi, so we do not want an in-memory database,
    # we would rather have that memeory available for computation.
    conn = sqlite3.connect('/etc/tiberius/settings.db')

    #This is the cursor that is used to execute SQL commands.
    c = conn.cursor()

    #Pi ID
    id = 0

    def deleteTables(self):
        try:
            self.c.execute('DROP TABLE pi_settings')
        except sqlite3.OperationalError:
            print(Fore.RED + 'Could not drop table pi_settings' + Fore.RESET)

        try:
            self.c.execute('DROP TABLE hw_versions')
        except sqlite3.OperationalError:
            print(Fore.RED + 'Could not drop table hw_versions' + Fore.RESET)

    def createTables(self):
        #Create table to store basic information about the Pi
        try:
            self.c.execute('''CREATE TABLE pi_settings
                 (id int primary key, created text, name text, ip_address text, hw_version int, description text)''')
        except sqlite3.OperationalError:
            print(Fore.RED + 'pi_settings table already exists' + Fore.RESET)

        try:
            #Stores information about the model og Pi being used
            self.c.execute('''CREATE TABLE hw_versions
                (created text, name text, memory int, clock int, description text)''')
        except sqlite3.OperationalError:
            print(Fore.RED + 'hw_versions table already exists' + Fore.RESET)

        #Set database properties
        self.c.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

    def getSetting(self, s):
        setting = (self.id,)
        self.c.execute('SELECT ' + s + ' FROM pi_settings WHERE id = ?', setting)
        return self.c.fetchone()[0]

    def setSetting(self, name, value):
        vals = (value, self.id,)
        self.c.execute("INSERT OR REPLACE INTO pi_settings (" + name + ", id) VALUES (?,?)", vals)
        self.conn.commit()
        return (value,)

    def getIPAddress(self):
        return self.getSetting("ip_address")

    def getName(self):
        return self.getSetting("name")

    def setName(self, value):
        self.setSetting('name', value)


# Test functions, for debugging only
if  __name__ =='__main__':
    settings = Settings()
    settings.deleteTables()
    settings.createTables()

    settings.setSetting('ip_address', '0.0.0.0')
    settings.setSetting('name', 'TestName')
    print 'ip_address: ', settings.getIPAddress()
    print 'name: ', settings.getName()
