import subprocess
import time

if __name__ == "__main__":
    print 'Running 'pon Server'
    r1 = subprocess.check_output(["pon Server"])
    print 'Waiting 10 seconds ...'
    time.sleep(10)
    print 'Running route add -net 10.113.211.0 netmask 255.255.255.0 dev ppp0'
    r2 = subprocess.check_output(["route add -net 10.113.211.0 netmask 255.255.255.0 dev ppp0"])
    print 'Results: '
    print r1
    print r2
