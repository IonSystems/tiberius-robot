Motor Control Architecture
==========================

Introduction
------------
Tiberius III and onwards use a new modular motor control system.
This new design was motivated by the need for a more reliable communication network.
Previously an I2C network was used to communicate between Raspberry Pis
and the MD03 motor drivers, but I2C does not cope well with interference,
when the motor drivers are under high torque.

Motor Control Architecture Diagram
----------------------------------
The following diagram illustrates the communication hierarchy of the new system:

.. figure::  images/udp_motor_control.png
   :align:   center

   UDP/CAN/I2C Motor Control Diagram

The `bridge` is bound to a port, listening for incoming UDP packets.
The UDP packets contain a sequence of bytes, passing on command information.
A description of how the sequence is decoded can be found in Table.

UDP Command Descriptor
----------------------

A full UDP command consists of 17 bytes, each byte is allocated as follows:

+------------+------------------+---------------------+-------------------------------------------+
| Seq. #     | Length (bytes)   | Name                | Description                               |
+============+==================+=====================+===========================================+
| 1          | 1                | Destination         | See :ref:`destination-identifiers`        |
+------------+------------------+---------------------+-------------------------------------------+
| 2          | 4                | Node Address        | See :ref:`node-addresses`                 |
+------------+------------------+---------------------+-------------------------------------------+
| 3          | 1                | Command ID          | See :ref:`command-identifiers`            |
+------------+------------------+---------------------+-------------------------------------------+
| 4          | 7                | Command Parameters  | Parameter data associated with command.   |
+------------+------------------+---------------------+-------------------------------------------+
| 5          | 4                | Number of CAN bytes | Number of bytes to forward in CAN packet. |
+------------+------------------+---------------------+-------------------------------------------+

.. _command-identifiers:

Command Identifiers
-------------------

+--------------------+------------------+------------------------------------------------------------------+
| Command            | Identifier       | Description                                                      |
+====================+==================+==================================================================+
| PID_P_GAIN         | 0x00             | Set the proportional gain of the motor PID controller.           |
+--------------------+------------------+------------------------------------------------------------------+
| TOGGLE_LED1        | 0x01             | Toggle LED1 on the addressed node.                               |
+--------------------+------------------+------------------------------------------------------------------+
| MOTOR_SPEED        | 0x02             | Set the desired motor speed for PID controller.                  |
+--------------------+------------------+------------------------------------------------------------------+
| MOTOR_PWM          | 0x03             | Set the motor motor PWM duty cycle (0 to 100).                   |
+--------------------+------------------+------------------------------------------------------------------+
| STEERING_MOVE_REL  | 0x04             | Change steering angle by an amount relative to current location. |
+--------------------+------------------+------------------------------------------------------------------+
| STEERING_MOVE_ABS  | 0x05             | Set the steering angle to a absolute angle.                      |
+--------------------+------------------+------------------------------------------------------------------+
| STEERING_ANGLE     | 0x06             | Set internal steering angle value.                               |
+--------------------+------------------+------------------------------------------------------------------+

.. _node-addresses:

Node Addresses
---------------

+--------------------+------------------+
| Node Position      | Identifier       |
+====================+==================+
| FRONT_LEFT         | 0x00             |
+--------------------+------------------+
| FRONT_RIGHT        | 0x01             |
+--------------------+------------------+
| REAR_LEFT          | 0x02             |
+--------------------+------------------+
| REAR_RIGHT         | 0x03             |
+--------------------+------------------+
| BRIDGE             | 0x04             |
+--------------------+------------------+

.. _destination-identifiers:

Command Destination Identifiers
-------------------------------

+--------------------+------------------+---------------------------------------------------------------+
| Destination        | Identifier       | Description                                                   |
+====================+==================+===============================================================+
| LOCAL              | 0x00             | Command is not destined for a CAN node, just the bridge node. |
+--------------------+------------------+---------------------------------------------------------------+
| CANBUS             | 0x40             | The command should be forwarded to the CAN bus,               |
|                    |                  | for another node to pick up.                                  |
+--------------------+------------------+---------------------------------------------------------------+

.. _motor_direction_identifiers:

Motor Direction Identifiers
---------------------------

+--------------------+------------------+
| Direction          | Identifier       |
+====================+==================+
| CLOCKWISE          | 0x00             |
+--------------------+------------------+
| ANTICLOCKWISE      | 0x01             |
+--------------------+------------------+

.. _steering_movement_type_identifiers:

Steering Movement Type Identifiers
----------------------------------

+--------------------+------------------+
| Movement Type      | Identifier       |
+====================+==================+
| ABSOLUTE           | 0x00             |
+--------------------+------------------+
| RELATIVE           | 0x01             |
+--------------------+------------------+
