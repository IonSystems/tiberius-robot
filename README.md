Tiberius Project (2015/16),
Heriot-Watt University,
Riccarton,
Edinburgh


#Introduction

Tiberius is an autonomous robot, the robot has been in development since 2005 by Masters students at Heriot-Watt University.

## Modules

### `control`
All software relating to the control of Tiberius, this includes everything from hardware drivers to control loops.
### `testing`
Unit test suite.
### `smbus-dummy`
A dummy I2C network for debugging purposes.
### `diagnostics`
Monitors the database transactions for data integrity.
### `logger`
Sets up Tiberius's logging settings, so that all modules can log in the same format.
### `utils`
Contains useful utility functions, specific to Tiberius.
# Documentation
Our wiki contains information about this project as well as user guides.

#Testing
Our testing module contains everything you need to test the functions of Tiberius.
It includes functional tests that requires Tiberius to be positioned at the start of the test environement. The tests will then run, checking that Tiberius is acting as it should.
