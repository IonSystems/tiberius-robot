Controlling Motors with Python and UDP
======================================

Introduction
------------

This tutorial will walk through the process of controlling Tiberius III's motors using the various interfaces available to you.
The interfaces available for use are:

- Direct UDP Control Script: A standalone script that sends UDP packets to an IP address.
- Keyboard Control Script: This script can be used both Tiberius II and III.
  Depends on the `control` module to select the correct communication method.
  Requires the user to SSH session to the target device.
- Web Interface: Requires the web interface to be running on a web server.
- Android Application (TODO): will interface with our Control API,
  in the same way the web interface does.

Control via Direct UDP Control Script
-------------------------------------

1. Turn Tiberius on

2. Connect your device (any Python compatible device) to Tiberius's network.

  - If Tiberius is configured as an access point, connect to it.
  - If Tiberius is connected to another access point, connect to it.

  .. note::
    There are many possible network configurations that cannot be listed here.
    The controlling device must have a path on the network to Tiberius.

3. Start the UDP Control Script on the controlling data_service

  - The script is here: `tiberius/testing/scripts/udp_control.py`

4. Use the WASD keys on your keyboard for
    forward, left, backward, right (respectively). Press the space bar to stop.
    We use *latching controls*, meaning Tiberius will remain in in motion
    after a key has been released. The space bar will put Tiberius
    in a STOP state until another state is triggered by the WASD keys.

Control via Keyboard Control script
-----------------------------------


Control via Web Interface
-------------------------

See :ref:`web-interface-tut-teleoperation`.

Control via Android Application
-------------------------------

.. note::
  All interfaces currently have no feedback, all packets are sent blindly,
  in the hope that a device is listening at the other end.

  An area of future work is to send an acknowledgement packet from the
  motor control bridge, so the controlling device can respond appropriately to
  the outcome of the communication.
