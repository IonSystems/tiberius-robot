# Terminal Control Interface
A python module that provides a simple interface to control Tiberius.
## Features
- Change and view settings
- Control movement
- Database queries
- Shutdown/restart individual Pi's
- Start/stop other modules
- Read sensor data

## Implemenation
Currently, the idea is to be able to run commands in the following manner, through SSH:
- ./tci.py -settings --ip_address=0.0.0.0 --name=Tiberius Prime
- ./tci.py -shutdown -all
- ./tci.py -list --table=devices
- ./tci.py -start --module=web-interface
- ./tci.py -test -all
- ./tci.py -move --dir=north --dis=10
- ./tci.py -rotate --bearing=129
- ./tci.py -rotate --relative=-10

## Use cases
- Used by the testing module to run automated functional testing.
- Used by developers for debugging and manual testing
- Provides a simple API which could be used to develop future control applications.
