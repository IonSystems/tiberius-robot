from control import Control
import sys, tty, termios, time

c = Control()


def getKey():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
if __name__ == "__main__":
    while(True):

        key = getKey()
        print "Key " + key + "pressed"
        if(key == 'c'):
            c.motors.stop()
            sys.exit(0)
        elif(key == 'w'):
            c.motors.setSpeed(50)
            c.motors.moveForward()
        elif(key == 'W'):
            c.motors.setSpeed(100)
            c.motors.moveForward()
        elif(key == 'a'):
            c.motors.setSpeed(40)
            c.motors.turnRight()
        elif(key == 'A'):
            c.motors.setSpeed(100)
            c.motors.turnRight()
        elif(key == 's'):
            c.motors.setSpeed(50)
            c.motors.moveBackward()
        elif(key == 'S'):
            c.motors.setSpeed(100)
            c.motors.moveBackward()
        elif(key == 'd'):
            c.motors.setSpeed(50)
            c.motors.turnLeft()
        elif(key == 'D'):
            c.motors.setSpeed(100)
            c.motors.turnLeft()
        

        time.sleep(0.1)
        c.motors.stop()
        

