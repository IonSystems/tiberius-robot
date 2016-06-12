Introduction
============

Testing
-------
The following commands will come in useful when testing an d debugging the control API:

* Send an HTTP GET request to the control API with an authorisation token:

  .. code-block:: none

     curl -v -H 'X-Auth-Token: ReplaceWithAuthToken'  http://10.113.211.244:8000/motors?forwards=50

  The above command will start all four motors at 50% speed.
  The IP address used is that of the Raspberry Pi running the control API.
  This will need changed to the correct IP address for your device.

* Start the WSGI Server:

    .. code-block:: none

      python api.py

    Or start via the quickstart script:

    .. code-block:: none

      python quickstart.py -a

Missions
--------

A Mission is a list of Tasks. Missions are designed by a user via the web interface.

Tasks
-----

A Task base class (ABC) was created to allow the easy integration of simple tasks to a Tiberius mission.
Each task must implement the following functions:

.. code-block:: python

  def runTask()
    pass

  def pauseTask()
    pass

  def resumeTask()
    pass

These are pretty self explanatory.
Each task must be able to be paused, depending on what the task is doing, this may be easy or more difficult to do.
