---
title: 53. System Views
id: views
---

In addition to the system catalogs, PostgreSQL provides a number of built-in views.
Some system views provide convenient access to some commonly used queries on the system catalogs.
Other views provide access to internal server state.

The information schema ([35. The Information Schema](braised:ref/information-schema)) provides an alternative set of views which overlap the functionality of the system views.
Since the information schema is SQL-standard whereas the views described here are PostgreSQL-specific, it\'s usually better to use the information schema if it provides all the information you need.

The following table lists the system views described here.
More detailed documentation of each view follows below.
There are some additional views that provide access to accumulated statistics; they are described in [Section 27.2](braised:ref/monitoring-stats).
