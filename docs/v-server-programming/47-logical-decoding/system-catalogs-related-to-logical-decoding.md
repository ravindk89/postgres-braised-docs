---
title: "47.5. System Catalogs Related to Logical Decoding"
id: logicaldecoding-catalogs
---

## System Catalogs Related to Logical Decoding

The [pg_replication_slots](#view-pg-replication-slots) view and the [pg_stat_replication](#monitoring-pg-stat-replication-view) view provide information about the current state of replication slots and streaming replication connections respectively.
These views apply to both physical and logical replication.
The [pg_stat_replication_slots](#monitoring-pg-stat-replication-slots-view) view provides statistics information about the logical replication slots.
