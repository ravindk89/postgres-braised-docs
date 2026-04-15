---
title: "47.4. Logical Decoding SQL Interface"
id: logicaldecoding-sql
---

## Logical Decoding SQL Interface

See [Replication Management Functions](braised:ref/functions-admin#replication-management-functions) for detailed documentation on the SQL-level API for interacting with logical decoding.

Synchronous replication (see [Synchronous Replication](braised:ref/warm-standby#synchronous-replication)) is only supported on replication slots used over the streaming replication interface.
The function interface and additional, non-core interfaces do not support synchronous replication.
