Mission Planning
================

Planning a mission is split into two stages:

Stage 1: Complete the new mission form, defining basic details
(name description of mission...)

Stage 2: Plot waypoints and assign tasks using the interactive map.

Stage 1: New mission form
-------------------------

1.      Give the mission a name and description

        .. figure::  images/mission_step_1.png
           :align:   center

           Step 1: Mission name and description

2.      Decide what platforms the mission should be compatible with.
        Bear in mind that different platforms support different tasks,
        and some platforms have a faster ground speed than others.

        .. figure::  images/mission_step_2.png
           :align:   center

           Step 2: Supported platforms

3.     Assign an auto-start time. This feature is not fully implemented yet,
       but in future releases it will be possible for a mission to automatically
       start at a predefined time, at an interval defined by the user.
       An example of a possible use case: Drive to a charging station every night.

       .. figure::  images/mission_step_3.png
          :align:   center

          Step 3: Schedule settings

4.     Proceed to the interactive map (Waypoint plotting).

       .. figure::  images/mission_step_4.png
          :align:   center

          Step 3: Proceed to the interactive map.

Stage 2: Waypoint plotting
--------------------------

Adding a Waypoint
^^^^^^^^^^^^^^^^^

Click anywhere on the map to add a waypoint to that location.

.. warning::
  Currently, there is no undo function.
  If a mistake is made, the only way to amend it is to start again by refreshing the page.
  This is a major inconvenience and will be fixed in future releases.

Adding a Task
^^^^^^^^^^^^^

Adding a task to a waypoint:

1. Click on a waypoint.
2. Select a task from the drop-down menu.
3. Click on the Add Task button.

.. warning::
  Currently, there is no way to remove a task once it has been added.
  If an incorrect task is added, it can only be removed by refreshing the page and starting again.
  This is a major inconvenience and will be fixed in future releases.
