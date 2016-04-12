Getting Started
===============

The following tutorial will guide you through all the steps necessary to build a system using compatible hardware, and getting the system up and running.
The instructions are ordered with the biggest steps at the start, so you don't get a head of yourself doing the easy bits at the beginning. In summary,
in order to get a robot up and running you will need to set up a network, make sure you have compatible hardware, get a hold of our software, and
configure our software for your hardware.

1. Installing compatible hardware

  The following pieces of hardware have been tested to work with the Tiberius Software Suite:

  - Raspberry Pi 1A+,1B,1B+,2B,3B
  - NEO-M8N_ (GPS Module, serial interface)
  - CMPS11_ (Tilt Compensated Compass, I2C interface supported)
  - RPLIDAR_ (LIDAR, basic scan supported)
  - MD03_ (Motor Driver, I2C interface supported)
  - RAMPS_ (3D Printer Driver Board, used to drive our robotic arm, serial interface)

  The exact model of DC motors used is not important, we have used wiper motors and motors from `Como Drills`_.

  Our software assumes you'll have four driven wheels, any other number of wheels will require modification of the software.
  However this shouldn't be too difficult - modification of actuators.py to add or remove motors.

  Here two of our vehicles to get an idea of what we're talking about:

  .. figure:: images/tibby-2.png
    :width: 800 px
    :scale: 50 %
    :alt: Tiberius II
    :align: center

    Tiberius II

  .. figure:: images/tibby-3.png
    :width: 800 px
    :scale: 50 %
    :alt: Tiberius III under construction
    :align: center

    Tiberius III

  A thorough `hardware installation tutorial`_ is available.



2. Getting a hold of the Tiberius software repository

  Once you have some hardware, you can think about getting a copy of our software.
  The way we would normally go about this is connecting the Raspberry Pi to the internet,
  through your LAN. The the separate tutorial (`Networking Tutorial`_) for network configuration instructions.

  .. note::
    It is *essential* to clone our git repository into into :code:`/home/pi/git/`.
    This should result in the following folder being created:

      :code:`/home/pi/git/tiberius-robot/`

    This is due to the hardcoded path names that are used in :code:`setup.py`, in order to move files into a known location.
    Yes, we know, we know. This is not by any means ideal, but it is what currently works. This is an area that could
    be looked into if you feel like contributing.

  Here's an example of the commands that we use to clone our repository
  (assuming that you are currently in your home directory):

  .. code:: bash

    cd git/
    git clone https://github.com/IonSystems/tiberius-robot.git

2. Installing the Tiberius Software Suite

  Now that you have the hardware and have cloned the repository, you can now think about installing our software.

  .. note::

    We have tried to make our setup script as thorough and reliable as possible, although we cannot guarantee success.
    Unless you have done some funny things to file permissions, it *should* work.

  You should now locate yourself in the top level of our repository using :code:`cd tiberius-robot/`. You can then run
  the setup script by typing :code:`sudo python setup.py install`. They above commands are provided below for copy-paste
  convenience:

  .. code:: bash

    cd tiberius-robot/
    sudo python setup.py install

3. Configuring your installation

  A number of configuration settings need to be edited to suit the particulars of your hardware setup.
  The configuration directory is the same for every installation, so your config file should appear in
  :code:`/etc/tiberius/tiberius_conf.conf`

  It is important to ensure the correct hardware is enabled, and unavailable hardware is disabled. As this
  configuration file is used by the software to determine whether or not to communicate with the respective device.
  The configuration file is also used by the API to decide whether or not to allow access to the particular device
  through the API.

  It is also important to ensure the correct ports are set for the enabled devices.
  There is a test script to detect the USB devices available here: :code:`tiberius/testing/scripts/gps_dev_path`.
  An alternative approach would be to run :code:`start_tiberius.py` and you'll know if the ports are wrong if you
  see error messages for the device in question.

  Last, but not least, ensure the I2C addresses are set correctly.
  To list all I2C slaves on the bus, run :code:`i2cdetect 1`. You'll need to work out the correspondence
  between the addresses and the devices by process of elimination, or by reading data sheets for default addresses.

4. Getting the software running

  This *should* be the easy part! We have a script in the top level of our repository called :code:`start_tiberius.py`.
  This script takes care of starting everything in the correct order. If this starts successfully,
  then there is a good chance that everything is now operational.

  For a more in-depth discussion of what :code:`start_tiberius.py` does, see docstrings.

.. _MD03:
.. _RPLIDAR:
.. _CMPS11: http://www.robot-electronics.co.uk/products/sensors/compass-sensors/cmps11-tilt-compensated-magnetic-compass.html
.. _NEO-M8N: http://www.drotek.com/shop/en/home/511-ublox-neo-m8-gps-module.html?search_query=gps&results=35
.. _RAMPS: http://reprap.org/wiki/RAMPS_1.4
.. _Como Drills: http://www.mfacomodrills.com/motors/motors.html
.. _Networking Tutorial : ./networking.html
.. _hardware installation tutorial : ./hardware_installation.html
