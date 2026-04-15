---
title: 24. Routine Database Maintenance Tasks
id: maintenance
---

PostgreSQL, like any database software, requires that certain tasks be performed regularly to achieve optimum performance.
The tasks discussed here are *required*, but they are repetitive in nature and can easily be automated using standard tools such as cron scripts or Windows\' Task Scheduler.
It is the database administrator\'s responsibility to set up appropriate scripts, and to check that they execute successfully.

One obvious maintenance task is the creation of backup copies of the data on a regular schedule.
Without a recent backup, you have no chance of recovery after a catastrophe (disk failure, fire, mistakenly dropping a critical table, etc.).
The backup and recovery mechanisms available in PostgreSQL are discussed at length in [25. Backup and Restore](braised:ref/backup).

The other main category of maintenance task is periodic "vacuuming" of the database.
This activity is discussed in [Section 24.1](braised:ref/routine-vacuuming).
Closely related to this is updating the statistics that will be used by the query planner, as discussed in [Section 24.1](braised:ref/routine-vacuuming).

Another task that might need periodic attention is log file management.
This is discussed in [Section 24.3](braised:ref/logfile-maintenance).

[check_postgres](https://bucardo.org/check_postgres/) is available for monitoring database health and reporting unusual conditions. check_postgres integrates with Nagios and MRTG, but can be run standalone too.

PostgreSQL is low-maintenance compared to some other database management systems.
Nonetheless, appropriate attention to these tasks will go far towards ensuring a pleasant and productive experience with the system.
