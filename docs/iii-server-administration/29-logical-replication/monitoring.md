---
title: "29.10. Monitoring"
id: logical-replication-monitoring
---

## Monitoring

Because logical replication is based on a similar architecture as [physical streaming replication](#streaming-replication), the monitoring on a publication node is similar to monitoring of a physical replication primary (see [Monitoring](braised:ref/warm-standby#monitoring)).

The monitoring information about subscription is visible in [pg_stat_subscription](#monitoring-pg-stat-subscription).
This view contains one row for every subscription worker.
A subscription can have zero or more active subscription workers depending on its state.

Normally, there is a single apply process running for an enabled subscription.
A disabled subscription or a crashed subscription will have zero rows in this view.
If the initial data synchronization of any table is in progress, there will be additional workers for the tables being synchronized.
Moreover, if the [`streaming`](#sql-createsubscription-params-with-streaming) transaction is applied in parallel, there may be additional parallel apply workers.
