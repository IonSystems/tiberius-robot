import traceback
import time

from tiberius.communications.antenna_positioning import Antenna

def antenna_thread():
    antenna = Antenna()
    while True:
        try:
            antenna.correct_heading()
            time.sleep(10)
        except Exception as e:
            traceback.print_exc()
            print e
