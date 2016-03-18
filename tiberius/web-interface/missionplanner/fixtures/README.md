# How to use fixtures


`python manage.py loaddata <name-of-fixture.json>`

Django looks in the app fixture directory by default, so that's where we keep our fixtures.

Fixtures can be generated using something similar to`python manage.py dumpdata > missionplanner/fixtures/all_data.json`

Or, for a specific Model:
`python manage.py dumpdata missionplanner.task > missionplanner/fixtures/tasks2.json`

## Example:

`python manage.py loaddata tasks.json`
