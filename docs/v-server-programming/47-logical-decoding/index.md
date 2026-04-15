---
title: 47. Logical Decoding
id: logicaldecoding
---

PostgreSQL provides infrastructure to stream the modifications performed via SQL to external consumers.
This functionality can be used for a variety of purposes, including replication solutions and auditing.

Changes are sent out in streams identified by logical replication slots.

The format in which those changes are streamed is determined by the output plugin used.
An example plugin is provided in the PostgreSQL distribution.
Additional plugins can be written to extend the choice of available formats without modifying any core code.
Every output plugin has access to each individual new row produced by `INSERT` and the new row version created by `UPDATE`.
Availability of old row versions for `UPDATE` and `DELETE` depends on the configured replica identity (see [ALTER TABLE](braised:ref/sql-altertable)).

Changes can be consumed either using the streaming replication protocol (see [Section 54.4](braised:ref/protocol-replication) and [Section 47.3](braised:ref/logicaldecoding-walsender)), or by calling functions via SQL (see [Section 47.4](braised:ref/logicaldecoding-sql)).
It is also possible to write additional methods of consuming the output of a replication slot without modifying core code (see [Section 47.7](braised:ref/logicaldecoding-writer)).
