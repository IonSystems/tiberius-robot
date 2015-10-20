import sqlite3
import datetime, time



def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

conn = sqlite3.connect('tiberius.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

def create_tables():
    c = conn.cursor()

    # Create gps_waypoint table
    c.execute('''DROP TABLE IF EXISTS gps_waypoint''')
    c.execute('''CREATE TABLE gps_waypoint
                 (d date,
                 t timestamp,
                 latitude real,
                 longitude real,
                 altitude real)''')

    # Create ultrasonic_reading table
    c.execute('''DROP TABLE IF EXISTS ultrasonic_reading''')
    c.execute('''CREATE TABLE ultrasonic_reading
                 (front_left real,
                 front_centre real,
                 front_right real,
                 rear_left real,
                 rear_centre real,
                 rear_right real)''')

    # Create motor_control table
    c.execute('''DROP TABLE IF EXISTS motor_control''')
    c.execute('''CREATE TABLE motor_control
                 (t timestamp,
                 front_left_speed_desired real,
                 front_right_speed_desired real,
                 rear_left_speed_desired real,
                 rear_right_speed_desired real,
                 front_left_angle_desired real,
                 front_right_angle_desired real,
                 rear_left_angle_desired real,
                 rear_right_angle_desired real)''')

    # Create lighting_control table
    c.execute('''DROP TABLE IF EXISTS lighting_control''')
    c.execute('''CREATE TABLE lighting_control
                 (beacon_red integer,
                 beacon_green integer,
                 beacon_blue integer,
                 headlights integer)''')



    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


if __name__ == "__main__":
    create_tables()
