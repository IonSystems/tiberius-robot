# Control API
## Introduction
The control API will run on a Raspberry Pi, on Tiberius. The API will allow connections from the Android application, web interface and other modules seeking control of Tiberius. All control MUST pass through the API in order to keep track of who and what has current control. Only one controlling connection is allowed at once, to prevent conflicting control. Other connections are allowed, but any control requests are ignored, non-controlling users can request sensor data and other non-controlling requests. Non-controlling connections may ask for control, and access will be transferred to that connection, if a valid control key is provided.

## Requirements
- The API should allow an application to move Tiberius forwards and backwards.
- The API should allow an application turn Tiberius by a relative amount of degrees.
- The API should allow an application to turn Tiberius to face a bearing.
- The API should return ultrasonic sensor data when requested.
  - The application should provide a time-stamp to retrieve the correct data.
- The API should return LIDAR point clouds when requested.
  - The application should provide a time-stamp to retrieve the correct point cloud.
  - The API will respond with the nearest point cloud to the time-stamp requested.
- The API should be expandable, allowing future developers to add support for more features.
- The API should not be too powerful.
  - The API should not allow individual control of the motors.
  - The API should not allow access to internal registers of I2C devices.
  - The API should not allow SQL database queries.
  - The API should not allow access to passwords or secret keys.
- The API should allow an application to move the robotic arm.
  - The API should allow an application to position the robotic arm at a specific x,y,z coordinate. (Cartesian Positioning)
  - The API should allow an application to define the angle of each arm in degrees.

  ## Implementation
  The API will be produced using the [Falcon framework](http://falconframework.org/). Documentation for the framework can be found [here](http://falcon.readthedocs.org/en/stable/).

  ## Running the API
  [gunicorn](http://gunicorn.org/) will be used to host the API. The server can easily be started by doing the following:

  `pip install gunicorn` to install gunicorn.

  `gunicorn app` To run your app with gunicorn. 'app' is the name of the python file.
