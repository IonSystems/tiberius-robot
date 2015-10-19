import subprocess
import time

if __name__ == "__main__":
    subprocess.check_output(["pon Server && route add -net 10.113.211.0 netmask 255.255.255.0 dev ppp0"])
    
