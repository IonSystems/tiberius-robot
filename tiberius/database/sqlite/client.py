import sqlite3


class DatabaseClient:

    def __init__(self):
        self.conn = sqlite3.connect(
            'tiberius.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    def close(self):
        self.conn.close()

    def setMotorValues(self, front_left, front_right, rear_left, rear_right):
        cur = self.conn.cursor()
        cur.execute("insert into motor_control(front_left_speed_desired,front_right_speed_desired,rear_left_speed_desired,rear_right_speed_desired) values (?, ?, ?, ?)",
                    (front_left, front_right, rear_left, rear_right))

    def getMotorValues(self):
        cur = self.conn.cursor()
        cur.execute(
            "select front_left_speed_desired,front_right_speed_desired,rear_left_speed_desired,rear_right_speed_desired from motor_control")
        row = cur.fetchone()
        result = {'fl': row[0], 'fr': row[1], 'rl': row[2], 'rr': row[3]}
        return result

if __name__ == "__main__":
    client = DatabaseClient()
    client.setMotorValues(2, 2, 2, 2)
    print client.getMotorValues()
    client.close()
