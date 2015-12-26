# Diagnostics
This module runs as a daemon on any of the Raspberry Pi's. It detects mechanical, electrical and software faults be reading sensor information from the database. As the daemon runs, a log is kept in the database. The diagnostics daemon also has super powers:
- Limit maximum speed
- Limit turning angle
- Disable motors
- Shutdown raspberry Pis
- Power off Tiberius
- Emergency broadcast
