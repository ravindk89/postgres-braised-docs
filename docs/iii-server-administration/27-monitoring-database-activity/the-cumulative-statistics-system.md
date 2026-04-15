---
title: "27.2. The Cumulative Statistics System"
id: monitoring-stats
---

## The Cumulative Statistics System

PostgreSQL\'s cumulative statistics system supports collection and reporting of information about server activity.
Presently, accesses to tables and indexes in both disk-block and individual-row terms are counted.
The total number of rows in each table, and information about vacuum and analyze actions for each table are also counted.
If enabled, calls to user-defined functions and the total time spent in each one are counted as well.

PostgreSQL also supports reporting dynamic information about exactly what is going on in the system right now, such as the exact command currently being executed by other server processes, and which other connections exist in the system.
This facility is independent of the cumulative statistics system.

### Statistics Collection Configuration

Since collection of statistics adds some overhead to query execution, the system can be configured to collect or not collect information.
This is controlled by configuration parameters that are normally set in `postgresql.conf`. (See [Server Configuration](#server-configuration) for details about setting configuration parameters.)

The parameter [track_activities (boolean)
      
       track_activities configuration parameter](braised:ref/runtime-config-statistics#track-activities-boolean-track-activities-configuration-parameter) enables monitoring of the current command being executed by any server process.

The parameter [track_cost_delay_timing (boolean)
      
       track_cost_delay_timing configuration parameter](braised:ref/runtime-config-statistics#track-cost-delay-timing-boolean-track-cost-delay-timing-configuration-parameter) enables monitoring of cost-based vacuum delay.

The parameter [track_counts (boolean)
      
       track_counts configuration parameter](braised:ref/runtime-config-statistics#track-counts-boolean-track-counts-configuration-parameter) controls whether cumulative statistics are collected about table and index accesses.

The parameter [track_functions (enum)
      
       track_functions configuration parameter](braised:ref/runtime-config-statistics#track-functions-enum-track-functions-configuration-parameter) enables tracking of usage of user-defined functions.

The parameter [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) enables monitoring of block read, write, extend, and fsync times.

The parameter [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) enables monitoring of WAL read, write and fsync times.

Normally these parameters are set in `postgresql.conf` so that they apply to all server processes, but it is possible to turn them on or off in individual sessions using the [SET](braised:ref/sql-set) command. (To prevent ordinary users from hiding their activity from the administrator, only superusers are allowed to change these parameters with `SET`.)

Cumulative statistics are collected in shared memory.
Every PostgreSQL process collects statistics locally, then updates the shared data at appropriate intervals.
When a server, including a physical replica, shuts down cleanly, a permanent copy of the statistics data is stored in the `pg_stat` subdirectory, so that statistics can be retained across server restarts.
In contrast, when starting from an unclean shutdown (e.g., after an immediate shutdown, a server crash, starting from a base backup, and point-in-time recovery), all statistics counters are reset.

### Viewing Statistics

Several predefined views, listed in Dynamic Statistics Views, are available to show the current state of the system.
There are also several other views, listed in Collected Statistics Views, available to show the accumulated statistics.
Alternatively, one can build custom views using the underlying cumulative statistics functions, as discussed in [Statistics Functions](#monitoring-stats-functions).

When using the cumulative statistics views and functions to monitor collected data, it is important to realize that the information does not update instantaneously.
Each individual server process flushes out accumulated statistics to shared memory just before going idle, but not more frequently than once per `PGSTAT_MIN_INTERVAL` milliseconds (1 second unless altered while building the server); so a query or transaction still in progress does not affect the displayed totals and the displayed information lags behind actual activity.
However, current-query information collected by `track_activities` is always up-to-date.

Another important point is that when a server process is asked to display any of the accumulated statistics, accessed values are cached until the end of its current transaction in the default configuration.
So the statistics will show static information as long as you continue the current transaction.
Similarly, information about the current queries of all sessions is collected when any such information is first requested within a transaction, and the same information will be displayed throughout the transaction.
This is a feature, not a bug, because it allows you to perform several queries on the statistics and correlate the results without worrying that the numbers are changing underneath you.
When analyzing statistics interactively, or with expensive queries, the time delta between accesses to individual statistics can lead to significant skew in the cached statistics.
To minimize skew, `stats_fetch_consistency` can be set to `snapshot`, at the price of increased memory usage for caching not-needed statistics data.
Conversely, if it\'s known that statistics are only accessed once, caching accessed statistics is unnecessary and can be avoided by setting `stats_fetch_consistency` to `none`.
You can invoke `pg_stat_clear_snapshot()` to discard the current transaction\'s statistics snapshot or cached values (if any).
The next use of statistical information will (when in snapshot mode) cause a new snapshot to be built or (when in cache mode) accessed statistics to be cached.

A transaction can also see its own statistics (not yet flushed out to the shared memory statistics) in the views pg_stat_xact_all_tables, pg_stat_xact_sys_tables, pg_stat_xact_user_tables, and pg_stat_xact_user_functions.
These numbers do not act as stated above; instead they update continuously throughout the transaction.

Some of the information in the dynamic statistics views shown in Dynamic Statistics Views is security restricted.
Ordinary users can only see all the information about their own sessions (sessions belonging to a role that they are a member of).
In rows about other sessions, many columns will be null.
Note, however, that the existence of a session and its general properties such as its sessions user and database are visible to all users.
Superusers and roles with privileges of built-in role [`pg_read_all_stats`](#predefined-role-pg-monitor) can see all the information about all sessions.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  View Name
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_activity
  :::{/cell}
  :::{.cell}
  One row per server process, showing information related to the current activity of that process, such as state and current query. See [pg_stat_activity](#monitoring-pg-stat-activity-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_replication
  :::{/cell}
  :::{.cell}
  One row per WAL sender process, showing statistics about replication to that sender\'s connected standby server. See [pg_stat_replication](#monitoring-pg-stat-replication-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_wal_receiver
  :::{/cell}
  :::{.cell}
  Only one row, showing statistics about the WAL receiver from that receiver\'s connected server. See [pg_stat_wal_receiver](#monitoring-pg-stat-wal-receiver-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_recovery_prefetch
  :::{/cell}
  :::{.cell}
  Only one row, showing statistics about blocks prefetched during recovery. See [pg_stat_recovery_prefetch](#monitoring-pg-stat-recovery-prefetch) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_subscription
  :::{/cell}
  :::{.cell}
  At least one row per subscription, showing information about the subscription workers. See [pg_stat_subscription](#monitoring-pg-stat-subscription) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_ssl
  :::{/cell}
  :::{.cell}
  One row per connection (regular and replication), showing information about SSL used on this connection. See [pg_stat_ssl](#monitoring-pg-stat-ssl-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_gssapi
  :::{/cell}
  :::{.cell}
  One row per connection (regular and replication), showing information about GSSAPI authentication and encryption used on this connection. See [pg_stat_gssapi](#monitoring-pg-stat-gssapi-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_analyze
  :::{/cell}
  :::{.cell}
  One row for each backend (including autovacuum worker processes) running `ANALYZE`, showing current progress. See [ANALYZE Progress Reporting](braised:ref/progress-reporting#analyze-progress-reporting).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_create_index
  :::{/cell}
  :::{.cell}
  One row for each backend running `CREATE INDEX` or `REINDEX`, showing current progress. See [CREATE INDEX Progress Reporting](braised:ref/progress-reporting#create-index-progress-reporting).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_vacuum
  :::{/cell}
  :::{.cell}
  One row for each backend (including autovacuum worker processes) running `VACUUM`, showing current progress. See [VACUUM Progress Reporting](braised:ref/progress-reporting#vacuum-progress-reporting).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_cluster
  :::{/cell}
  :::{.cell}
  One row for each backend running `CLUSTER` or `VACUUM FULL`, showing current progress. See [CLUSTER Progress Reporting](braised:ref/progress-reporting#cluster-progress-reporting).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_basebackup
  :::{/cell}
  :::{.cell}
  One row for each WAL sender process streaming a base backup, showing current progress. See [Base Backup Progress Reporting](braised:ref/progress-reporting#base-backup-progress-reporting).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_progress_copy
  :::{/cell}
  :::{.cell}
  One row for each backend running `COPY`, showing current progress. See [COPY Progress Reporting](braised:ref/progress-reporting#copy-progress-reporting).
  :::{/cell}
  :::{/row}
:::{/table}

  : Dynamic Statistics Views

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  View Name
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_archiver
  :::{/cell}
  :::{.cell}
  One row only, showing statistics about the WAL archiver process\'s activity. See [pg_stat_archiver](#monitoring-pg-stat-archiver-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_bgwriter
  :::{/cell}
  :::{.cell}
  One row only, showing statistics about the background writer process\'s activity. See [pg_stat_bgwriter](#monitoring-pg-stat-bgwriter-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_checkpointer
  :::{/cell}
  :::{.cell}
  One row only, showing statistics about the checkpointer process\'s activity. See [pg_stat_checkpointer](#monitoring-pg-stat-checkpointer-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_database
  :::{/cell}
  :::{.cell}
  One row per database, showing database-wide statistics. See [pg_stat_database](#monitoring-pg-stat-database-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_database_conflicts
  :::{/cell}
  :::{.cell}
  One row per database, showing database-wide statistics about query cancels due to conflict with recovery on standby servers. See [pg_stat_database_conflicts](#monitoring-pg-stat-database-conflicts-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_io
  :::{/cell}
  :::{.cell}
  One row for each combination of backend type, context, and target object containing cluster-wide I/O statistics. See [pg_stat_io](#monitoring-pg-stat-io-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_replication_slots
  :::{/cell}
  :::{.cell}
  One row per replication slot, showing statistics about the replication slot\'s usage. See [pg_stat_replication_slots](#monitoring-pg-stat-replication-slots-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_slru
  :::{/cell}
  :::{.cell}
  One row per SLRU, showing statistics of operations. See [pg_stat_slru](#monitoring-pg-stat-slru-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_subscription_stats
  :::{/cell}
  :::{.cell}
  One row per subscription, showing statistics about errors and conflicts. See [pg_stat_subscription_stats](#monitoring-pg-stat-subscription-stats) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_wal
  :::{/cell}
  :::{.cell}
  One row only, showing statistics about WAL activity. See [pg_stat_wal](#monitoring-pg-stat-wal-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_all_tables
  :::{/cell}
  :::{.cell}
  One row for each table in the current database, showing statistics about accesses to that specific table. See [pg_stat_all_tables](#monitoring-pg-stat-all-tables-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_sys_tables
  :::{/cell}
  :::{.cell}
  Same as pg_stat_all_tables, except that only system tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_user_tables
  :::{/cell}
  :::{.cell}
  Same as pg_stat_all_tables, except that only user tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_xact_all_tables
  :::{/cell}
  :::{.cell}
  Similar to pg_stat_all_tables, but counts actions taken so far within the current transaction (which are *not* yet included in pg_stat_all_tables and related views). The columns for numbers of live and dead rows and vacuum and analyze actions are not present in this view.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_xact_sys_tables
  :::{/cell}
  :::{.cell}
  Same as pg_stat_xact_all_tables, except that only system tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_xact_user_tables
  :::{/cell}
  :::{.cell}
  Same as pg_stat_xact_all_tables, except that only user tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_all_indexes
  :::{/cell}
  :::{.cell}
  One row for each index in the current database, showing statistics about accesses to that specific index. See [pg_stat_all_indexes](#monitoring-pg-stat-all-indexes-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_sys_indexes
  :::{/cell}
  :::{.cell}
  Same as pg_stat_all_indexes, except that only indexes on system tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_user_indexes
  :::{/cell}
  :::{.cell}
  Same as pg_stat_all_indexes, except that only indexes on user tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_user_functions
  :::{/cell}
  :::{.cell}
  One row for each tracked function, showing statistics about executions of that function. See [pg_stat_user_functions](#monitoring-pg-stat-user-functions-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_stat_xact_user_functions
  :::{/cell}
  :::{.cell}
  Similar to pg_stat_user_functions, but counts only calls during the current transaction (which are *not* yet included in pg_stat_user_functions).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_all_tables
  :::{/cell}
  :::{.cell}
  One row for each table in the current database, showing statistics about I/O on that specific table. See [pg_statio_all_tables](#monitoring-pg-statio-all-tables-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_sys_tables
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_tables, except that only system tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_user_tables
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_tables, except that only user tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_all_indexes
  :::{/cell}
  :::{.cell}
  One row for each index in the current database, showing statistics about I/O on that specific index. See [pg_statio_all_indexes](#monitoring-pg-statio-all-indexes-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_sys_indexes
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_indexes, except that only indexes on system tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_user_indexes
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_indexes, except that only indexes on user tables are shown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_all_sequences
  :::{/cell}
  :::{.cell}
  One row for each sequence in the current database, showing statistics about I/O on that specific sequence. See [pg_statio_all_sequences](#monitoring-pg-statio-all-sequences-view) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_sys_sequences
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_sequences, except that only system sequences are shown. (Presently, no system sequences are defined, so this view is always empty.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_statio_user_sequences
  :::{/cell}
  :::{.cell}
  Same as pg_statio_all_sequences, except that only user sequences are shown.
  :::{/cell}
  :::{/row}
:::{/table}

  : Collected Statistics Views

The per-index statistics are particularly useful to determine which indexes are being used and how effective they are.

The pg_stat_io and pg_statio\_ set of views are useful for determining the effectiveness of the buffer cache. They can be used to calculate a cache hit ratio. Note that while PostgreSQL\'s I/O statistics capture most instances in which the kernel was invoked in order to perform I/O, they do not differentiate between data which had to be fetched from disk and that which already resided in the kernel page cache. Users are advised to use the PostgreSQL statistics views in combination with operating system utilities for a more complete picture of their database\'s I/O performance.

### pg_stat_activity

The pg_stat_activity view will have one row per server process, showing information related to the current activity of that process.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datid `oid`

   OID of the database this backend is connected to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datname `name`

   Name of the database this backend is connected to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of this backend
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   leader_pid `integer`

   Process ID of the parallel group leader if this process is a parallel query worker, or process ID of the leader apply worker if this process is a parallel apply worker. `NULL` indicates that this process is a parallel group leader or leader apply worker, or does not participate in any parallel operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usesysid `oid`

   OID of the user logged into this backend
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usename `name`

   Name of the user logged into this backend
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   application_name `text`

   Name of the application that is connected to this backend
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_addr `inet`

   IP address of the client connected to this backend. If this field is null, it indicates either that the client is connected via a Unix socket on the server machine or that this is an internal process such as autovacuum.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_hostname `text`

   Host name of the connected client, as reported by a reverse DNS lookup of client_addr. This field will only be non-null for IP connections, and only when [log_hostname (boolean)
      
       log_hostname configuration parameter](braised:ref/runtime-config-logging#log-hostname-boolean-log-hostname-configuration-parameter) is enabled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_port `integer`

   TCP port number that the client is using for communication with this backend, or `-1` if a Unix socket is used. If this field is null, it indicates that this is an internal server process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_start `timestamp with time zone`

   Time when this process was started. For client backends, this is the time the client connected to the server.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   xact_start `timestamp with time zone`

   Time when this process\' current transaction was started, or null if no transaction is active. If the current query is the first of its transaction, this column is equal to the query_start column.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   query_start `timestamp with time zone`

   Time when the currently active query was started, or if state is not `active`, when the last query was started
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   state_change `timestamp with time zone`

   Time when the state was last changed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wait_event_type `text`

   The type of event for which the backend is waiting, if any; otherwise NULL. See Wait Event Types.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wait_event `text`

   Wait event name if backend is currently waiting, otherwise NULL. See Wait Events of Type  through Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   state `text`

   Current overall state of this backend. Possible values are:

   -   `starting`: The backend is in initial startup. Client authentication is performed during this phase.

   -   `active`: The backend is executing a query.

   -   `idle`: The backend is waiting for a new client command.

   -   `idle in transaction`: The backend is in a transaction, but is not currently executing a query.

   -   `idle in transaction (aborted)`: This state is similar to `idle in transaction`, except one of the statements in the transaction caused an error.

   -   `fastpath function call`: The backend is executing a fast-path function.

   -   `disabled`: This state is reported if [track_activities (boolean)
      
       track_activities configuration parameter](braised:ref/runtime-config-statistics#track-activities-boolean-track-activities-configuration-parameter) is disabled in this backend.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_xid `xid`

   Top-level transaction identifier of this backend, if any; see [Transactions and Identifiers](braised:ref/transaction-id).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_xmin `xid`

   The current backend\'s `xmin` horizon.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   query_id `bigint`

   Identifier of this backend\'s most recent query. If state is `active` this field shows the identifier of the currently executing query. In all other states, it shows the identifier of last query that was executed. Query identifiers are not computed by default so this field will be null unless [compute_query_id (enum)
      
       compute_query_id configuration parameter](braised:ref/runtime-config-statistics#compute-query-id-enum-compute-query-id-configuration-parameter) parameter is enabled or a third-party module that computes query identifiers is configured.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   query `text`

   Text of this backend\'s most recent query. If state is `active` this field shows the currently executing query. In all other states, it shows the last query that was executed. By default the query text is truncated at 1024 bytes; this value can be changed via the parameter [track_activity_query_size (integer)
      
       track_activity_query_size configuration parameter](braised:ref/runtime-config-statistics#track-activity-query-size-integer-track-activity-query-size-configuration-parameter).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_type `text`

   Type of current backend. Possible types are `autovacuum launcher`, `autovacuum worker`, `logical replication launcher`, `logical replication worker`, `parallel worker`, `background writer`, `client backend`, `checkpointer`, `archiver`, `standalone backend`, `startup`, `walreceiver`, `walsender`, `walwriter` and `walsummarizer`. In addition, background workers registered by extensions may have additional types.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_activity View

:::{.callout type="note"}
The wait_event and state columns are independent. If a backend is in the `active` state, it may or may not be `waiting` on some event. If the state is `active` and wait_event is non-null, it means that a query is being executed, but is being blocked somewhere in the system. To keep the reporting overhead low, the system does not attempt to synchronize different aspects of activity data for a backend. As a result, ephemeral discrepancies may exist between the view\'s columns.
:::

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Wait Event Type
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Activity`
  :::{/cell}
  :::{.cell}
  The server process is idle. This event type indicates a process waiting for activity in its main processing loop. `wait_event` will identify the specific wait point; see Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferPin`
  :::{/cell}
  :::{.cell}
  The server process is waiting for exclusive access to a data buffer. Buffer pin waits can be protracted if another process holds an open cursor that last read data from the buffer in question. See [Wait Event Types](#wait-event-types).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Client`
  :::{/cell}
  :::{.cell}
  The server process is waiting for activity on a socket connected to a user application. Thus, the server expects something to happen that is independent of its internal processes. `wait_event` will identify the specific wait point; see Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Extension`
  :::{/cell}
  :::{.cell}
  The server process is waiting for some condition defined by an extension module. See Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `InjectionPoint`
  :::{/cell}
  :::{.cell}
  The server process is waiting for an injection point to reach an outcome defined in a test. See [Injection Points](braised:ref/xfunc-c#injection-points) for more details. This type has no predefined wait points.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `IO`
  :::{/cell}
  :::{.cell}
  The server process is waiting for an I/O operation to complete. `wait_event` will identify the specific wait point; see Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `IPC`
  :::{/cell}
  :::{.cell}
  The server process is waiting for some interaction with another server process. `wait_event` will identify the specific wait point; see Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Lock`
  :::{/cell}
  :::{.cell}
  The server process is waiting for a heavyweight lock. Heavyweight locks, also known as lock manager locks or simply locks, primarily protect SQL-visible objects such as tables. However, they are also used to ensure mutual exclusion for certain internal operations such as relation extension. `wait_event` will identify the type of lock awaited; see Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LWLock`
  :::{/cell}
  :::{.cell}
  The server process is waiting for a lightweight lock. Most such locks protect a particular data structure in shared memory. `wait_event` will contain a name identifying the purpose of the lightweight lock. (Some locks have specific names; others are part of a group of locks each with a similar purpose.) See Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Timeout`
  :::{/cell}
  :::{.cell}
  The server process is waiting for a timeout to expire. `wait_event` will identify the specific wait point; see Wait Events of Type .
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Event Types

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Activity` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ArchiverMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of archiver process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AutovacuumMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of autovacuum launcher process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BgwriterHibernate`
  :::{/cell}
  :::{.cell}
  Waiting in background writer process, hibernating.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BgwriterMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of background writer process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointerMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of checkpointer process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointerShutdown`
  :::{/cell}
  :::{.cell}
  Waiting for checkpointer process to be terminated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `IoWorkerMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of IO Worker process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalApplyMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of logical replication apply process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalLauncherMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of logical replication launcher process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalParallelApplyMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of logical replication parallel apply process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryWalStream`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of startup process for WAL to arrive, during streaming recovery.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotsyncMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of slot synchronization.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotsyncShutdown`
  :::{/cell}
  :::{.cell}
  Waiting for slot sync worker to shut down.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SysloggerMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of syslogger process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalReceiverMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of WAL receiver process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSenderMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of WAL sender process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSummarizerWal`
  :::{/cell}
  :::{.cell}
  Waiting in WAL summarizer for more WAL to be generated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalWriterMain`
  :::{/cell}
  :::{.cell}
  Waiting in main loop of WAL writer process.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Activity`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Buffer` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferCleanup`
  :::{/cell}
  :::{.cell}
  Waiting to acquire an exclusive pin on a buffer. Buffer pin waits can be protracted if another process holds an open cursor that last read data from the buffer in question.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferExclusive`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a exclusive lock on a buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferShared`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a shared lock on a buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferShareExclusive`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a share exclusive lock on a buffer.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Buffer`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Client` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ClientRead`
  :::{/cell}
  :::{.cell}
  Waiting to read data from the client.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ClientWrite`
  :::{/cell}
  :::{.cell}
  Waiting to write data to the client.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `GssOpenServer`
  :::{/cell}
  :::{.cell}
  Waiting to read data from the client while establishing a GSSAPI session.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LibpqwalreceiverConnect`
  :::{/cell}
  :::{.cell}
  Waiting in WAL receiver to establish connection to remote server.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LibpqwalreceiverReceive`
  :::{/cell}
  :::{.cell}
  Waiting in WAL receiver to receive data from remote server.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SslOpenServer`
  :::{/cell}
  :::{.cell}
  Waiting for SSL while attempting connection.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitForStandbyConfirmation`
  :::{/cell}
  :::{.cell}
  Waiting for WAL to be received and flushed by the physical standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitForWalFlush`
  :::{/cell}
  :::{.cell}
  Waiting for WAL flush to reach a target LSN on a primary or standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitForWalReplay`
  :::{/cell}
  :::{.cell}
  Waiting for WAL replay to reach a target LSN on a standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitForWalWrite`
  :::{/cell}
  :::{.cell}
  Waiting for WAL write to reach a target LSN on a standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSenderWaitForWal`
  :::{/cell}
  :::{.cell}
  Waiting for WAL to be flushed in WAL sender process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSenderWriteData`
  :::{/cell}
  :::{.cell}
  Waiting for any activity when processing replies from WAL receiver in WAL sender process.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Client`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Extension` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Extension`
  :::{/cell}
  :::{.cell}
  Waiting in an extension.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Extension`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `IO` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AioIoCompletion`
  :::{/cell}
  :::{.cell}
  Waiting for another process to complete IO.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AioIoUringExecution`
  :::{/cell}
  :::{.cell}
  Waiting for IO execution via io_uring.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AioIoUringSubmit`
  :::{/cell}
  :::{.cell}
  Waiting for IO submission via io_uring.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BasebackupRead`
  :::{/cell}
  :::{.cell}
  Waiting for base backup to read from a file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BasebackupSync`
  :::{/cell}
  :::{.cell}
  Waiting for data written by a base backup to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BasebackupWrite`
  :::{/cell}
  :::{.cell}
  Waiting for base backup to write to a file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BuffileRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a buffered file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BuffileTruncate`
  :::{/cell}
  :::{.cell}
  Waiting for a buffered file to be truncated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BuffileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to a buffered file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFileRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from the `pg_control` file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFileSync`
  :::{/cell}
  :::{.cell}
  Waiting for the `pg_control` file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFileSyncUpdate`
  :::{/cell}
  :::{.cell}
  Waiting for an update to the `pg_control` file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to the `pg_control` file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFileWriteUpdate`
  :::{/cell}
  :::{.cell}
  Waiting for a write to update the `pg_control` file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CopyFileCopy`
  :::{/cell}
  :::{.cell}
  Waiting for a file copy operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CopyFileRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read during a file copy operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CopyFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write during a file copy operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CopyFromRead`
  :::{/cell}
  :::{.cell}
  Waiting to read data from a pipe, a file or a program during COPY FROM.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CopyToWrite`
  :::{/cell}
  :::{.cell}
  Waiting to write data to a pipe, a file or a program during COPY TO.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileExtend`
  :::{/cell}
  :::{.cell}
  Waiting for a relation data file to be extended.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileFlush`
  :::{/cell}
  :::{.cell}
  Waiting for a relation data file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileImmediateSync`
  :::{/cell}
  :::{.cell}
  Waiting for an immediate synchronization of a relation data file to durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFilePrefetch`
  :::{/cell}
  :::{.cell}
  Waiting for an asynchronous prefetch from a relation data file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a relation data file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileSync`
  :::{/cell}
  :::{.cell}
  Waiting for changes to a relation data file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileTruncate`
  :::{/cell}
  :::{.cell}
  Waiting for a relation data file to be truncated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DataFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to a relation data file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DsmAllocate`
  :::{/cell}
  :::{.cell}
  Waiting for a dynamic shared memory segment to be allocated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DsmFillZeroWrite`
  :::{/cell}
  :::{.cell}
  Waiting to fill a dynamic shared memory backing file with zeroes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileAddtodatadirRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read while adding a line to the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileAddtodatadirSync`
  :::{/cell}
  :::{.cell}
  Waiting for data to reach durable storage while adding a line to the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileAddtodatadirWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write while adding a line to the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileCreateRead`
  :::{/cell}
  :::{.cell}
  Waiting to read while creating the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileCreateSync`
  :::{/cell}
  :::{.cell}
  Waiting for data to reach durable storage while creating the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileCreateWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write while creating the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFileRecheckdatadirRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read during recheck of the data directory lock file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteCheckpointSync`
  :::{/cell}
  :::{.cell}
  Waiting for logical rewrite mappings to reach durable storage during a checkpoint.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteMappingSync`
  :::{/cell}
  :::{.cell}
  Waiting for mapping data to reach durable storage during a logical rewrite.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteMappingWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of mapping data during a logical rewrite.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteSync`
  :::{/cell}
  :::{.cell}
  Waiting for logical rewrite mappings to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteTruncate`
  :::{/cell}
  :::{.cell}
  Waiting for truncate of mapping data during a logical rewrite.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRewriteWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of logical rewrite mappings.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RelationMapRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of the relation map file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RelationMapReplace`
  :::{/cell}
  :::{.cell}
  Waiting for durable replacement of a relation map file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RelationMapWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to the relation map file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReorderBufferRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read during reorder buffer management.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReorderBufferWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write during reorder buffer management.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReorderLogicalMappingRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of a logical mapping during reorder buffer management.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a replication slot control file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotRestoreSync`
  :::{/cell}
  :::{.cell}
  Waiting for a replication slot control file to reach durable storage while restoring it to memory.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotSync`
  :::{/cell}
  :::{.cell}
  Waiting for a replication slot control file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to a replication slot control file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SlruFlushSync`
  :::{/cell}
  :::{.cell}
  Waiting for SLRU data to reach durable storage during a checkpoint or database shutdown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SlruRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of an SLRU page.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SlruSync`
  :::{/cell}
  :::{.cell}
  Waiting for SLRU data to reach durable storage following a page write.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SlruWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of an SLRU page.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SnapbuildRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of a serialized historical catalog snapshot.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SnapbuildSync`
  :::{/cell}
  :::{.cell}
  Waiting for a serialized historical catalog snapshot to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SnapbuildWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of a serialized historical catalog snapshot.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TimelineHistoryFileSync`
  :::{/cell}
  :::{.cell}
  Waiting for a timeline history file received via streaming replication to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TimelineHistoryFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of a timeline history file received via streaming replication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TimelineHistoryRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of a timeline history file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TimelineHistorySync`
  :::{/cell}
  :::{.cell}
  Waiting for a newly created timeline history file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TimelineHistoryWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of a newly created timeline history file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TwophaseFileRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read of a two phase state file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TwophaseFileSync`
  :::{/cell}
  :::{.cell}
  Waiting for a two phase state file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TwophaseFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of a two phase state file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `VersionFileSync`
  :::{/cell}
  :::{.cell}
  Waiting for the version file to reach durable storage while creating a database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `VersionFileWrite`
  :::{/cell}
  :::{.cell}
  Waiting for the version file to be written while creating a database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalsenderTimelineHistoryRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a timeline history file during a walsender timeline command.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalBootstrapSync`
  :::{/cell}
  :::{.cell}
  Waiting for WAL to reach durable storage during bootstrapping.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalBootstrapWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write of a WAL page during bootstrapping.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalCopyRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read when creating a new WAL segment by copying an existing one.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalCopySync`
  :::{/cell}
  :::{.cell}
  Waiting for a new WAL segment created by copying an existing one to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalCopyWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write when creating a new WAL segment by copying an existing one.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalInitSync`
  :::{/cell}
  :::{.cell}
  Waiting for a newly initialized WAL file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalInitWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write while initializing a new WAL file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a WAL file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSummaryRead`
  :::{/cell}
  :::{.cell}
  Waiting for a read from a WAL summary file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSummaryWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to a WAL summary file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSync`
  :::{/cell}
  :::{.cell}
  Waiting for a WAL file to reach durable storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSyncMethodAssign`
  :::{/cell}
  :::{.cell}
  Waiting for data to reach durable storage while assigning a new WAL sync method.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalWrite`
  :::{/cell}
  :::{.cell}
  Waiting for a write to a WAL file.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Io`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `IPC` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AppendReady`
  :::{/cell}
  :::{.cell}
  Waiting for subplan nodes of an `Append` plan node to be ready.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ArchiveCleanupCommand`
  :::{/cell}
  :::{.cell}
  Waiting for [archive_cleanup_command (string)
      
        archive_cleanup_command configuration parameter](braised:ref/runtime-config-wal#archive-cleanup-command-string-archive-cleanup-command-configuration-parameter) to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ArchiveCommand`
  :::{/cell}
  :::{.cell}
  Waiting for [archive_command (string)
      
       archive_command configuration parameter](braised:ref/runtime-config-wal#archive-command-string-archive-command-configuration-parameter) to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BackendTermination`
  :::{/cell}
  :::{.cell}
  Waiting for the termination of another backend.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BackupWaitWalArchive`
  :::{/cell}
  :::{.cell}
  Waiting for WAL files required for a backup to be successfully archived.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BgworkerShutdown`
  :::{/cell}
  :::{.cell}
  Waiting for background worker to shut down.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BgworkerStartup`
  :::{/cell}
  :::{.cell}
  Waiting for background worker to start up.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BtreePage`
  :::{/cell}
  :::{.cell}
  Waiting for the page number needed to continue a parallel B-tree scan to become available.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferIo`
  :::{/cell}
  :::{.cell}
  Waiting for buffer I/O to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointDelayComplete`
  :::{/cell}
  :::{.cell}
  Waiting for a backend that blocks a checkpoint from completing.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointDelayStart`
  :::{/cell}
  :::{.cell}
  Waiting for a backend that blocks a checkpoint from starting.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointDone`
  :::{/cell}
  :::{.cell}
  Waiting for a checkpoint to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointStart`
  :::{/cell}
  :::{.cell}
  Waiting for a checkpoint to start.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ExecuteGather`
  :::{/cell}
  :::{.cell}
  Waiting for activity from a child process while executing a `Gather` plan node.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBatchAllocate`
  :::{/cell}
  :::{.cell}
  Waiting for an elected Parallel Hash participant to allocate a hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBatchElect`
  :::{/cell}
  :::{.cell}
  Waiting to elect a Parallel Hash participant to allocate a hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBatchLoad`
  :::{/cell}
  :::{.cell}
  Waiting for other Parallel Hash participants to finish loading a hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBuildAllocate`
  :::{/cell}
  :::{.cell}
  Waiting for an elected Parallel Hash participant to allocate the initial hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBuildElect`
  :::{/cell}
  :::{.cell}
  Waiting to elect a Parallel Hash participant to allocate the initial hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBuildHashInner`
  :::{/cell}
  :::{.cell}
  Waiting for other Parallel Hash participants to finish hashing the inner relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashBuildHashOuter`
  :::{/cell}
  :::{.cell}
  Waiting for other Parallel Hash participants to finish partitioning the outer relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBatchesDecide`
  :::{/cell}
  :::{.cell}
  Waiting to elect a Parallel Hash participant to decide on future batch growth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBatchesElect`
  :::{/cell}
  :::{.cell}
  Waiting to elect a Parallel Hash participant to allocate more batches.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBatchesFinish`
  :::{/cell}
  :::{.cell}
  Waiting for an elected Parallel Hash participant to decide on future batch growth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBatchesReallocate`
  :::{/cell}
  :::{.cell}
  Waiting for an elected Parallel Hash participant to allocate more batches.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBatchesRepartition`
  :::{/cell}
  :::{.cell}
  Waiting for other Parallel Hash participants to finish repartitioning.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBucketsElect`
  :::{/cell}
  :::{.cell}
  Waiting to elect a Parallel Hash participant to allocate more buckets.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBucketsReallocate`
  :::{/cell}
  :::{.cell}
  Waiting for an elected Parallel Hash participant to finish allocating more buckets.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `HashGrowBucketsReinsert`
  :::{/cell}
  :::{.cell}
  Waiting for other Parallel Hash participants to finish inserting tuples into new buckets.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalApplySendData`
  :::{/cell}
  :::{.cell}
  Waiting for a logical replication leader apply process to send data to a parallel apply process.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalParallelApplyStateChange`
  :::{/cell}
  :::{.cell}
  Waiting for a logical replication parallel apply process to change state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalSyncData`
  :::{/cell}
  :::{.cell}
  Waiting for a logical replication remote server to send data for initial table synchronization.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalSyncStateChange`
  :::{/cell}
  :::{.cell}
  Waiting for a logical replication remote server to change state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MessageQueueInternal`
  :::{/cell}
  :::{.cell}
  Waiting for another process to be attached to a shared message queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MessageQueuePutMessage`
  :::{/cell}
  :::{.cell}
  Waiting to write a protocol message to a shared message queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MessageQueueReceive`
  :::{/cell}
  :::{.cell}
  Waiting to receive bytes from a shared message queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MessageQueueSend`
  :::{/cell}
  :::{.cell}
  Waiting to send bytes to a shared message queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultixactCreation`
  :::{/cell}
  :::{.cell}
  Waiting for a multixact creation to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelBitmapScan`
  :::{/cell}
  :::{.cell}
  Waiting for parallel bitmap scan to become initialized.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelCreateIndexScan`
  :::{/cell}
  :::{.cell}
  Waiting for parallel `CREATE INDEX` workers to finish heap scan.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelFinish`
  :::{/cell}
  :::{.cell}
  Waiting for parallel workers to finish computing.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ProcarrayGroupUpdate`
  :::{/cell}
  :::{.cell}
  Waiting for the group leader to clear the transaction ID at transaction end.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ProcSignalBarrier`
  :::{/cell}
  :::{.cell}
  Waiting for a barrier event to be processed by all backends.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Promote`
  :::{/cell}
  :::{.cell}
  Waiting for standby promotion.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryConflictSnapshot`
  :::{/cell}
  :::{.cell}
  Waiting for recovery conflict resolution for a vacuum cleanup.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryConflictTablespace`
  :::{/cell}
  :::{.cell}
  Waiting for recovery conflict resolution for dropping a tablespace.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryEndCommand`
  :::{/cell}
  :::{.cell}
  Waiting for [recovery_end_command (string)
      
        recovery_end_command configuration parameter](braised:ref/runtime-config-wal#recovery-end-command-string-recovery-end-command-configuration-parameter) to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryPause`
  :::{/cell}
  :::{.cell}
  Waiting for recovery to be resumed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationOriginDrop`
  :::{/cell}
  :::{.cell}
  Waiting for a replication origin to become inactive so it can be dropped.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotDrop`
  :::{/cell}
  :::{.cell}
  Waiting for a replication slot to become inactive so it can be dropped.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RestoreCommand`
  :::{/cell}
  :::{.cell}
  Waiting for [restore_command (string)
      
        restore_command configuration parameter](braised:ref/runtime-config-wal#restore-command-string-restore-command-configuration-parameter) to complete.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SafeSnapshot`
  :::{/cell}
  :::{.cell}
  Waiting to obtain a valid snapshot for a `READ ONLY DEFERRABLE` transaction.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SyncRep`
  :::{/cell}
  :::{.cell}
  Waiting for confirmation from a remote server during synchronous replication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalReceiverExit`
  :::{/cell}
  :::{.cell}
  Waiting for the WAL receiver to exit.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalReceiverWaitStart`
  :::{/cell}
  :::{.cell}
  Waiting for startup process to send initial data for streaming replication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSummaryReady`
  :::{/cell}
  :::{.cell}
  Waiting for a new WAL summary to be generated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `XactGroupUpdate`
  :::{/cell}
  :::{.cell}
  Waiting for the group leader to update transaction status at transaction end.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Ipc`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Lock` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `advisory`
  :::{/cell}
  :::{.cell}
  Waiting to acquire an advisory user lock.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `applytransaction`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a lock on a remote transaction being applied by a logical replication subscriber.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `extend`
  :::{/cell}
  :::{.cell}
  Waiting to extend a relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `frozenid`
  :::{/cell}
  :::{.cell}
  Waiting to update pg_database.datfrozenxid and pg_database.datminmxid.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a lock on a non-relation database object.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `page`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a lock on a page of a relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `relation`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a lock on a relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `spectoken`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a speculative insertion lock.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `transactionid`
  :::{/cell}
  :::{.cell}
  Waiting for a transaction to finish.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `tuple`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a lock on a tuple.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `userlock`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a user lock.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `virtualxid`
  :::{/cell}
  :::{.cell}
  Waiting to acquire a virtual transaction ID lock; see [Transactions and Identifiers](braised:ref/transaction-id).
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Lock`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `LWLock` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AddinShmemInit`
  :::{/cell}
  :::{.cell}
  Waiting to manage an extension\'s space allocation in shared memory.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AioUringCompletion`
  :::{/cell}
  :::{.cell}
  Waiting for another process to complete IO via io_uring.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AioWorkerSubmissionQueue`
  :::{/cell}
  :::{.cell}
  Waiting to access AIO worker submission queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AutoFile`
  :::{/cell}
  :::{.cell}
  Waiting to update the `postgresql.auto.conf` file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `Autovacuum`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the current state of autovacuum workers.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `AutovacuumSchedule`
  :::{/cell}
  :::{.cell}
  Waiting to ensure that a table selected for autovacuum still needs vacuuming.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BackgroundWorker`
  :::{/cell}
  :::{.cell}
  Waiting to read or update background worker state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BtreeVacuum`
  :::{/cell}
  :::{.cell}
  Waiting to read or update vacuum-related information for a B-tree index.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BufferMapping`
  :::{/cell}
  :::{.cell}
  Waiting to associate a data block with a buffer in the buffer pool.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointerComm`
  :::{/cell}
  :::{.cell}
  Waiting to manage fsync requests.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CommitTs`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the last value set for a transaction commit timestamp.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CommitTsBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a commit timestamp SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CommitTsSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the commit timestamp SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ControlFile`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the `pg_control` file or create a new WAL file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DSMRegistry`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the dynamic shared memory registry.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DSMRegistryDSA`
  :::{/cell}
  :::{.cell}
  Waiting to access dynamic shared memory registry\'s dynamic shared memory allocator.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DSMRegistryHash`
  :::{/cell}
  :::{.cell}
  Waiting to access dynamic shared memory registry\'s shared hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `DynamicSharedMemoryControl`
  :::{/cell}
  :::{.cell}
  Waiting to read or update dynamic shared memory allocation information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `InjectionPoint`
  :::{/cell}
  :::{.cell}
  Waiting to read or update information related to injection points.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockFastPath`
  :::{/cell}
  :::{.cell}
  Waiting to read or update a process\' fast-path lock information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LockManager`
  :::{/cell}
  :::{.cell}
  Waiting to read or update information about "heavyweight" locks.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalDecodingControl`
  :::{/cell}
  :::{.cell}
  Waiting to read or update logical decoding status information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRepLauncherDSA`
  :::{/cell}
  :::{.cell}
  Waiting to access logical replication launcher\'s dynamic shared memory allocator.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRepLauncherHash`
  :::{/cell}
  :::{.cell}
  Waiting to access logical replication launcher\'s shared hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `LogicalRepWorker`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the state of logical replication workers.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactGen`
  :::{/cell}
  :::{.cell}
  Waiting to read or update shared multixact state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactMemberBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a multixact member SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactMemberSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the multixact member SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactOffsetBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a multixact offset SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactOffsetSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the multixact offset SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `MultiXactTruncation`
  :::{/cell}
  :::{.cell}
  Waiting to read or truncate multixact information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `NotifyBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a `NOTIFY` message SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `NotifyChannelHash`
  :::{/cell}
  :::{.cell}
  Waiting to access the `NOTIFY` channel hash table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `NotifyQueue`
  :::{/cell}
  :::{.cell}
  Waiting to read or update `NOTIFY` messages.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `NotifyQueueTail`
  :::{/cell}
  :::{.cell}
  Waiting to update limit on `NOTIFY` message storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `NotifySLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the `NOTIFY` message SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `OidGen`
  :::{/cell}
  :::{.cell}
  Waiting to allocate a new OID.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelAppend`
  :::{/cell}
  :::{.cell}
  Waiting to choose the next subplan during Parallel Append plan execution.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelBtreeScan`
  :::{/cell}
  :::{.cell}
  Waiting to synchronize workers during Parallel B-tree scan plan execution.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelHashJoin`
  :::{/cell}
  :::{.cell}
  Waiting to synchronize workers during Parallel Hash Join plan execution.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelQueryDSA`
  :::{/cell}
  :::{.cell}
  Waiting for parallel query dynamic shared memory allocation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ParallelVacuumDSA`
  :::{/cell}
  :::{.cell}
  Waiting for parallel vacuum dynamic shared memory allocation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PerSessionDSA`
  :::{/cell}
  :::{.cell}
  Waiting for parallel query dynamic shared memory allocation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PerSessionRecordType`
  :::{/cell}
  :::{.cell}
  Waiting to access a parallel query\'s information about composite types.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PerSessionRecordTypmod`
  :::{/cell}
  :::{.cell}
  Waiting to access a parallel query\'s information about type modifiers that identify anonymous record types.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PerXactPredicateList`
  :::{/cell}
  :::{.cell}
  Waiting to access the list of predicate locks held by the current serializable transaction during a parallel query.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PgStatsData`
  :::{/cell}
  :::{.cell}
  Waiting for shared memory stats data access.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PgStatsDSA`
  :::{/cell}
  :::{.cell}
  Waiting for stats dynamic shared memory allocator access.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PgStatsHash`
  :::{/cell}
  :::{.cell}
  Waiting for stats shared memory hash table access.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PredicateLockManager`
  :::{/cell}
  :::{.cell}
  Waiting to access predicate lock information used by serializable transactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ProcArray`
  :::{/cell}
  :::{.cell}
  Waiting to access the shared per-process data structures (typically, to get a snapshot or report a session\'s transaction ID).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RelationMapping`
  :::{/cell}
  :::{.cell}
  Waiting to read or update a `pg_filenode.map` file (used to track the filenode assignments of certain system catalogs).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RelCacheInit`
  :::{/cell}
  :::{.cell}
  Waiting to read or update a `pg_internal.init` relation cache initialization file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationOrigin`
  :::{/cell}
  :::{.cell}
  Waiting to create, drop or use a replication origin.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationOriginState`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the progress of one replication origin.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotAllocation`
  :::{/cell}
  :::{.cell}
  Waiting to allocate or free a replication slot.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotControl`
  :::{/cell}
  :::{.cell}
  Waiting to read or update replication slot state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ReplicationSlotIO`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a replication slot.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerialBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a serializable transaction conflict SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerialControl`
  :::{/cell}
  :::{.cell}
  Waiting to read or update shared `pg_serial` state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerializableFinishedList`
  :::{/cell}
  :::{.cell}
  Waiting to access the list of finished serializable transactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerializablePredicateList`
  :::{/cell}
  :::{.cell}
  Waiting to access the list of predicate locks held by serializable transactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerializableXactHash`
  :::{/cell}
  :::{.cell}
  Waiting to read or update information about serializable transactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SerialSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the serializable transaction conflict SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SharedTidBitmap`
  :::{/cell}
  :::{.cell}
  Waiting to access a shared TID bitmap during a parallel bitmap index scan.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SharedTupleStore`
  :::{/cell}
  :::{.cell}
  Waiting to access a shared tuple store during parallel query.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `ShmemIndex`
  :::{/cell}
  :::{.cell}
  Waiting to find or allocate space in shared memory.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SInvalRead`
  :::{/cell}
  :::{.cell}
  Waiting to retrieve messages from the shared catalog invalidation queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SInvalWrite`
  :::{/cell}
  :::{.cell}
  Waiting to add a message to the shared catalog invalidation queue.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SubtransBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a sub-transaction SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SubtransSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the sub-transaction SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SyncRep`
  :::{/cell}
  :::{.cell}
  Waiting to read or update information about the state of synchronous replication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SyncScan`
  :::{/cell}
  :::{.cell}
  Waiting to select the starting location of a synchronized table scan.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TablespaceCreate`
  :::{/cell}
  :::{.cell}
  Waiting to create or drop a tablespace.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `TwoPhaseState`
  :::{/cell}
  :::{.cell}
  Waiting to read or update the state of prepared transactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitEventCustom`
  :::{/cell}
  :::{.cell}
  Waiting to read or update custom wait events information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WaitLSN`
  :::{/cell}
  :::{.cell}
  Waiting to read or update shared Wait-for-LSN state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WALBufMapping`
  :::{/cell}
  :::{.cell}
  Waiting to replace a page in WAL buffers.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WALInsert`
  :::{/cell}
  :::{.cell}
  Waiting to insert WAL data into a memory buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WALSummarizer`
  :::{/cell}
  :::{.cell}
  Waiting to read or update WAL summarization state.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WALWrite`
  :::{/cell}
  :::{.cell}
  Waiting for WAL buffers to be written to disk.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WrapLimitsVacuum`
  :::{/cell}
  :::{.cell}
  Waiting to update limits on transaction id and multixact consumption.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `XactBuffer`
  :::{/cell}
  :::{.cell}
  Waiting for I/O on a transaction status SLRU buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `XactSLRU`
  :::{/cell}
  :::{.cell}
  Waiting to access the transaction status SLRU cache.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `XactTruncation`
  :::{/cell}
  :::{.cell}
  Waiting to execute `pg_xact_status` or update the oldest transaction ID available to it.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `XidGen`
  :::{/cell}
  :::{.cell}
  Waiting to allocate a new transaction ID.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Lwlock`

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  `Timeout` Wait Event
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `BaseBackupThrottle`
  :::{/cell}
  :::{.cell}
  Waiting during base backup when throttling activity.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CheckpointWriteDelay`
  :::{/cell}
  :::{.cell}
  Waiting between writes while performing a checkpoint.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `CommitDelay`
  :::{/cell}
  :::{.cell}
  Waiting for commit delay before WAL flush.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `PgSleep`
  :::{/cell}
  :::{.cell}
  Waiting due to a call to `pg_sleep` or a sibling function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryApplyDelay`
  :::{/cell}
  :::{.cell}
  Waiting to apply WAL during recovery because of a delay setting.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RecoveryRetrieveRetryInterval`
  :::{/cell}
  :::{.cell}
  Waiting during recovery when WAL data is not available from any source (`pg_wal`, archive or stream).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `RegisterSyncRequest`
  :::{/cell}
  :::{.cell}
  Waiting while sending synchronization requests to the checkpointer, because the request queue is full.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `SpinDelay`
  :::{/cell}
  :::{.cell}
  Waiting while acquiring a contended spinlock.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `VacuumDelay`
  :::{/cell}
  :::{.cell}
  Waiting in a cost-based vacuum delay point.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `VacuumTruncate`
  :::{/cell}
  :::{.cell}
  Waiting to acquire an exclusive lock to truncate off any empty pages at the end of a table vacuumed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `WalSummarizerError`
  :::{/cell}
  :::{.cell}
  Waiting after a WAL summarizer error.
  :::{/cell}
  :::{/row}
:::{/table}

  : Wait Events of Type `Timeout`

Here are examples of how wait events can be viewed:

    SELECT pid, wait_event_type, wait_event FROM pg_stat_activity WHERE wait_event is NOT NULL;
     pid  | wait_event_type | wait_event
    ------+-----------------+------------
     2540 | Lock            | relation
     6644 | LWLock          | ProcArray
    (2 rows)

    SELECT a.pid, a.wait_event, w.description
      FROM pg_stat_activity a JOIN
           pg_wait_events w ON (a.wait_event_type = w.type AND
                                a.wait_event = w.name)
      WHERE a.wait_event is NOT NULL and a.state = 'active';
    -[ RECORD 1 ]------------------------------------------------------​------------
    pid         | 686674
    wait_event  | WALInitSync
    description | Waiting for a newly initialized WAL file to reach durable storage

:::{.callout type="note"}
Extensions can add `Extension`, `InjectionPoint`, and `LWLock` events to the lists shown in Wait Events of Type  and Wait Events of Type . In some cases, the name of an `LWLock` assigned by an extension will not be available in all server processes. It might be reported as just "`extension`" rather than the extension-assigned name.
:::

### pg_stat_replication

The pg_stat_replication view will contain one row per WAL sender process, showing statistics about replication to that sender\'s connected standby server.
Only directly connected standbys are listed; no information is available about downstream standby servers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of a WAL sender process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usesysid `oid`

   OID of the user logged into this WAL sender process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usename `name`

   Name of the user logged into this WAL sender process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   application_name `text`

   Name of the application that is connected to this WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_addr `inet`

   IP address of the client connected to this WAL sender. If this field is null, it indicates that the client is connected via a Unix socket on the server machine.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_hostname `text`

   Host name of the connected client, as reported by a reverse DNS lookup of client_addr. This field will only be non-null for IP connections, and only when [log_hostname (boolean)
      
       log_hostname configuration parameter](braised:ref/runtime-config-logging#log-hostname-boolean-log-hostname-configuration-parameter) is enabled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_port `integer`

   TCP port number that the client is using for communication with this WAL sender, or `-1` if a Unix socket is used
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_start `timestamp with time zone`

   Time when this process was started, i.e., when the client connected to this WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_xmin `xid`

   This standby\'s `xmin` horizon reported by [hot_standby_feedback (boolean)
      
       hot_standby_feedback configuration parameter](braised:ref/runtime-config-replication#hot-standby-feedback-boolean-hot-standby-feedback-configuration-parameter).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   state `text`

   Current WAL sender state. Possible values are:

   -   `startup`: This WAL sender is starting up.

   -   `catchup`: This WAL sender\'s connected standby is catching up with the primary.

   -   `streaming`: This WAL sender is streaming changes after its connected standby server has caught up with the primary.

   -   `backup`: This WAL sender is sending a backup.

   -   `stopping`: This WAL sender is stopping.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sent_lsn `pg_lsn`

   Last write-ahead log location sent on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   write_lsn `pg_lsn`

   Last write-ahead log location written to disk by this standby server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   flush_lsn `pg_lsn`

   Last write-ahead log location flushed to disk by this standby server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   replay_lsn `pg_lsn`

   Last write-ahead log location replayed into the database on this standby server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   write_lag `interval`

   Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written it (but not yet flushed it or applied it). This can be used to gauge the delay that `synchronous_commit` level `remote_write` incurred while committing if this server was configured as a synchronous standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   flush_lag `interval`

   Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written and flushed it (but not yet applied it). This can be used to gauge the delay that `synchronous_commit` level `on` incurred while committing if this server was configured as a synchronous standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   replay_lag `interval`

   Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written, flushed and applied it. This can be used to gauge the delay that `synchronous_commit` level `remote_apply` incurred while committing if this server was configured as a synchronous standby.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sync_priority `integer`

   Priority of this standby server for being chosen as the synchronous standby in a priority-based synchronous replication. This has no effect in a quorum-based synchronous replication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sync_state `text`

   Synchronous state of this standby server. Possible values are:

   -   `async`: This standby server is asynchronous.

   -   `potential`: This standby server is now asynchronous, but can potentially become synchronous if one of current synchronous ones fails.

   -   `sync`: This standby server is synchronous.

   -   `quorum`: This standby server is considered as a candidate for quorum standbys.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reply_time `timestamp with time zone`

   Send time of last reply message received from standby server
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_replication View

The lag times reported in the pg_stat_replication view are measurements of the time taken for recent WAL to be written, flushed and replayed and for the sender to know about it. These times represent the commit delay that was (or would have been) introduced by each synchronous commit level, if the remote server was configured as a synchronous standby. For an asynchronous standby, the replay_lag column approximates the delay before recent transactions became visible to queries. If the standby server has entirely caught up with the sending server and there is no more WAL activity, the most recently measured lag times will continue to be displayed for a short time and then show NULL.

Lag times work automatically for physical replication. Logical decoding plugins may optionally emit tracking messages; if they do not, the tracking mechanism will simply display NULL lag.

:::{.callout type="note"}
The reported lag times are not predictions of how long it will take for the standby to catch up with the sending server assuming the current rate of replay. Such a system would show similar times while new WAL is being generated, but would differ when the sender becomes idle. In particular, when the standby has caught up completely, pg_stat_replication shows the time taken to write, flush and replay the most recent reported WAL location rather than zero as some users might expect. This is consistent with the goal of measuring synchronous commit and transaction visibility delays for recent write transactions. To reduce confusion for users expecting a different model of lag, the lag columns revert to NULL after a short time on a fully replayed idle system. Monitoring systems should choose whether to represent this as missing data, zero or continue to display the last known value.
:::

### pg_stat_replication_slots

The pg_stat_replication_slots view will contain one row per logical replication slot, showing statistics about its usage.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   slot_name `text`

   A unique, cluster-wide identifier for the replication slot
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spill_txns `bigint`

   Number of transactions spilled to disk once the memory used by logical decoding to decode changes from WAL has exceeded `logical_decoding_work_mem`. The counter gets incremented for both top-level transactions and subtransactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spill_count `bigint`

   Number of times transactions were spilled to disk while decoding changes from WAL for this slot. This counter is incremented each time a transaction is spilled, and the same transaction may be spilled multiple times.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spill_bytes `bigint`

   Amount of decoded transaction data spilled to disk while performing decoding of changes from WAL for this slot. This and other spill counters can be used to gauge the I/O which occurred during logical decoding and allow tuning `logical_decoding_work_mem`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stream_txns `bigint`

   Number of in-progress transactions streamed to the decoding output plugin after the memory used by logical decoding to decode changes from WAL for this slot has exceeded `logical_decoding_work_mem`. Streaming only works with top-level transactions (subtransactions can\'t be streamed independently), so the counter is not incremented for subtransactions.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stream_count`bigint`

   Number of times in-progress transactions were streamed to the decoding output plugin while decoding changes from WAL for this slot. This counter is incremented each time a transaction is streamed, and the same transaction may be streamed multiple times.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stream_bytes`bigint`

   Amount of transaction data decoded for streaming in-progress transactions to the decoding output plugin while decoding changes from WAL for this slot. This and other streaming counters for this slot can be used to tune `logical_decoding_work_mem`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_txns `bigint`

   Number of decoded transactions sent to the decoding output plugin for this slot. This counts top-level transactions only, and is not incremented for subtransactions. Note that this includes the transactions that are streamed and/or spilled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_bytes`bigint`

   Amount of transaction data decoded for sending transactions to the decoding output plugin while decoding changes from WAL for this slot. Note that this includes data that is streamed and/or spilled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_replication_slots View

### pg_stat_wal_receiver

The pg_stat_wal_receiver view will contain only one row, showing statistics about the WAL receiver from that receiver\'s connected server.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of the WAL receiver process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   status `text`

   Activity status of the WAL receiver process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   receive_start_lsn `pg_lsn`

   First write-ahead log location used when WAL receiver is started
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   receive_start_tli `integer`

   First timeline number used when WAL receiver is started
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   written_lsn `pg_lsn`

   Last write-ahead log location already received and written to disk, but not flushed. This should not be used for data integrity checks.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   flushed_lsn `pg_lsn`

   Last write-ahead log location already received and flushed to disk, the initial value of this field being the first log location used when WAL receiver is started
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   received_tli `integer`

   Timeline number of last write-ahead log location received and flushed to disk, the initial value of this field being the timeline number of the first log location used when WAL receiver is started
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_msg_send_time `timestamp with time zone`

   Send time of last message received from origin WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_msg_receipt_time `timestamp with time zone`

   Receipt time of last message received from origin WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   latest_end_lsn `pg_lsn`

   Last write-ahead log location reported to origin WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   latest_end_time `timestamp with time zone`

   Time of last write-ahead log location reported to origin WAL sender
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   slot_name `text`

   Replication slot name used by this WAL receiver
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sender_host `text`

   Host of the PostgreSQL instance this WAL receiver is connected to. This can be a host name, an IP address, or a directory path if the connection is via Unix socket. (The path case can be distinguished because it will always be an absolute path, beginning with `/`.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sender_port `integer`

   Port number of the PostgreSQL instance this WAL receiver is connected to.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conninfo `text`

   Connection string used by this WAL receiver, with security-sensitive fields obfuscated.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_wal_receiver View

### pg_stat_recovery_prefetch

The pg_stat_recovery_prefetch view will contain only one row. The columns wal_distance, block_distance and io_depth show current values, and the other columns show cumulative counters that can be reset with the `pg_stat_reset_shared` function.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prefetch `bigint`

   Number of blocks prefetched because they were not in the buffer pool
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hit `bigint`

   Number of blocks not prefetched because they were already in the buffer pool
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   skip_init `bigint`

   Number of blocks not prefetched because they would be zero-initialized
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   skip_new `bigint`

   Number of blocks not prefetched because they didn\'t exist yet
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   skip_fpw `bigint`

   Number of blocks not prefetched because a full page image was included in the WAL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   skip_rep `bigint`

   Number of blocks not prefetched because they were already recently prefetched
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_distance `int`

   How many bytes ahead the prefetcher is looking
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   block_distance `int`

   How many blocks ahead the prefetcher is looking
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   io_depth `int`

   How many prefetches have been initiated but are not yet known to have completed
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_recovery_prefetch View

### pg_stat_subscription

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subid `oid`

   OID of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subname `name`

   Name of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   worker_type `text`

   Type of the subscription worker process. Possible types are `apply`, `parallel apply`, and `table synchronization`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of the subscription worker process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   leader_pid `integer`

   Process ID of the leader apply worker if this process is a parallel apply worker; NULL if this process is a leader apply worker or a table synchronization worker
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of the relation that the worker is synchronizing; NULL for the leader apply worker and parallel apply workers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   received_lsn `pg_lsn`

   Last write-ahead log location received, the initial value of this field being 0; NULL for parallel apply workers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_msg_send_time `timestamp with time zone`

   Send time of last message received from origin WAL sender; NULL for parallel apply workers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_msg_receipt_time `timestamp with time zone`

   Receipt time of last message received from origin WAL sender; NULL for parallel apply workers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   latest_end_lsn `pg_lsn`

   Last write-ahead log location reported to origin WAL sender; NULL for parallel apply workers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   latest_end_time `timestamp with time zone`

   Time of last write-ahead log location reported to origin WAL sender; NULL for parallel apply workers
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_subscription View

### pg_stat_subscription_stats

The pg_stat_subscription_stats view will contain one row per subscription.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subid `oid`

   OID of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subname `name`

   Name of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   apply_error_count `bigint`

   Number of times an error occurred while applying changes. Note that any conflict resulting in an apply error will be counted in both `apply_error_count` and the corresponding conflict count (e.g., `confl_*`).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sync_error_count `bigint`

   Number of times an error occurred during the initial table synchronization
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_insert_exists `bigint`

   Number of times a row insertion violated a `NOT DEFERRABLE` unique constraint during the application of changes. See [insert_exists](braised:ref/logical-replication-conflicts#insert-exists) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_update_origin_differs `bigint`

   Number of times an update was applied to a row that had been previously modified by another source during the application of changes. See [update_origin_differs](braised:ref/logical-replication-conflicts#update-origin-differs) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_update_exists `bigint`

   Number of times that an updated row value violated a `NOT DEFERRABLE` unique constraint during the application of changes. See [update_exists](braised:ref/logical-replication-conflicts#update-exists) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_update_missing `bigint`

   Number of times the tuple to be updated was not found during the application of changes. See [update_missing](braised:ref/logical-replication-conflicts#update-missing) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_delete_origin_differs `bigint`

   Number of times a delete operation was applied to row that had been previously modified by another source during the application of changes. See [delete_origin_differs](braised:ref/logical-replication-conflicts#delete-origin-differs) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_delete_missing `bigint`

   Number of times the tuple to be deleted was not found during the application of changes. See [delete_missing](braised:ref/logical-replication-conflicts#delete-missing) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_multiple_unique_conflicts `bigint`

   Number of times a row insertion or an updated row values violated multiple `NOT DEFERRABLE` unique constraints during the application of changes. See [multiple_unique_conflicts](braised:ref/logical-replication-conflicts#multiple-unique-conflicts) for details about this conflict.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_subscription_stats View

### pg_stat_ssl

The pg_stat_ssl view will contain one row per backend or WAL sender process, showing statistics about SSL usage on this connection. It can be joined to pg_stat_activity or pg_stat_replication on the pid column to get more details about the connection.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of a backend or WAL sender process
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ssl `boolean`

   True if SSL is used on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   version `text`

   Version of SSL in use, or NULL if SSL is not in use on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cipher `text`

   Name of SSL cipher in use, or NULL if SSL is not in use on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   bits `integer`

   Number of bits in the encryption algorithm used, or NULL if SSL is not used on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_dn `text`

   Distinguished Name (DN) field from the client certificate used, or NULL if no client certificate was supplied or if SSL is not in use on this connection. This field is truncated if the DN field is longer than `NAMEDATALEN` (64 characters in a standard build).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   client_serial `numeric`

   Serial number of the client certificate, or NULL if no client certificate was supplied or if SSL is not in use on this connection. The combination of certificate serial number and certificate issuer uniquely identifies a certificate (unless the issuer erroneously reuses serial numbers).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   issuer_dn `text`

   DN of the issuer of the client certificate, or NULL if no client certificate was supplied or if SSL is not in use on this connection. This field is truncated like client_dn.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_ssl View

### pg_stat_gssapi

The pg_stat_gssapi view will contain one row per backend, showing information about GSSAPI usage on this connection. It can be joined to pg_stat_activity or pg_stat_replication on the pid column to get more details about the connection.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `integer`

   Process ID of a backend
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   gss_authenticated `boolean`

   True if GSSAPI authentication was used for this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   principal `text`

   Principal used to authenticate this connection, or NULL if GSSAPI was not used to authenticate this connection. This field is truncated if the principal is longer than `NAMEDATALEN` (64 characters in a standard build).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   encrypted `boolean`

   True if GSSAPI encryption is in use on this connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   credentials_delegated `boolean`

   True if GSSAPI credentials were delegated on this connection.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_gssapi View

### pg_stat_archiver

The pg_stat_archiver view will always have a single row, containing data about the archiver process of the cluster.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   archived_count `bigint`

   Number of WAL files that have been successfully archived
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_archived_wal `text`

   Name of the WAL file most recently successfully archived
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_archived_time `timestamp with time zone`

   Time of the most recent successful archive operation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   failed_count `bigint`

   Number of failed attempts for archiving WAL files
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_failed_wal `text`

   Name of the WAL file of the most recent failed archival operation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_failed_time `timestamp with time zone`

   Time of the most recent failed archival operation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_archiver View

Normally, WAL files are archived in order, oldest to newest, but that is not guaranteed, and does not hold under special circumstances like when promoting a standby or after crash recovery. Therefore it is not safe to assume that all files older than last_archived_wal have also been successfully archived.

### pg_stat_io

The pg_stat_io view will contain one row for each combination of backend type, target I/O object, and I/O context, showing cluster-wide I/O statistics. Combinations which do not make sense are omitted.

Currently, I/O on relations (e.g. tables, indexes) and WAL activity are tracked. However, relation I/O which bypasses shared buffers (e.g. when moving a table from one tablespace to another) is currently not tracked.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   backend_type `text`

   Type of backend (e.g. background worker, autovacuum worker). See [pg_stat_activity](#monitoring-pg-stat-activity-view) for more information on `backend_type`s. Some `backend_type`s do not accumulate I/O operation statistics and will not be included in the view.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   object `text`

   Target object of an I/O operation. Possible values are:

   -   `relation`: Permanent relations.

   -   `temp relation`: Temporary relations.

   -   `wal`: Write Ahead Logs.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   context `text`

   The context of an I/O operation. Possible values are:

   -   `normal`: The default or standard `context` for a type of I/O operation. For example, by default, relation data is read into and written out from shared buffers. Thus, reads and writes of relation data to and from shared buffers are tracked in `context` `normal`.

   -   `init`: I/O operations performed while creating the WAL segments are tracked in `context` `init`.

   -   `vacuum`: I/O operations performed outside of shared buffers while vacuuming and analyzing permanent relations. Temporary table vacuums use the same local buffer pool as other temporary table I/O operations and are tracked in `context` `normal`.

   -   `bulkread`: Certain large read I/O operations done outside of shared buffers, for example, a sequential scan of a large table.

   -   `bulkwrite`: Certain large write I/O operations done outside of shared buffers, such as `COPY`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reads `bigint`

   Number of read operations.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   read_bytes `numeric`

   The total size of read operations in bytes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   read_time `double precision`

   Time spent waiting for read operations in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled and `object` is not `wal`, or if [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) is enabled and `object` is `wal`, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   writes `bigint`

   Number of write operations.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   write_bytes `numeric`

   The total size of write operations in bytes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   write_time `double precision`

   Time spent waiting for write operations in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled and `object` is not `wal`, or if [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) is enabled and `object` is `wal`, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   writebacks `bigint`

   Number of units of size `BLCKSZ` (typically 8kB) which the process requested the kernel write out to permanent storage.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   writeback_time `double precision`

   Time spent waiting for writeback operations in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled, otherwise zero). This includes the time spent queueing write-out requests and, potentially, the time spent to write out the dirty data.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extends `bigint`

   Number of relation extend operations.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extend_bytes `numeric`

   The total size of relation extend operations in bytes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extend_time `double precision`

   Time spent waiting for extend operations in milliseconds. (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled and `object` is not `wal`, or if [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) is enabled and `object` is `wal`, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hits `bigint`

   The number of times a desired block was found in a shared buffer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evictions `bigint`

   Number of times a block has been written out from a shared or local buffer in order to make it available for another use.

   In `context` `normal`, this counts the number of times a block was evicted from a buffer and replaced with another block. In `context`s `bulkwrite`, `bulkread`, and `vacuum`, this counts the number of times a block was evicted from shared buffers in order to add the shared buffer to a separate, size-limited ring buffer for use in a bulk I/O operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reuses `bigint`

   The number of times an existing buffer in a size-limited ring buffer outside of shared buffers was reused as part of an I/O operation in the `bulkread`, `bulkwrite`, or `vacuum` `context`s.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fsyncs `bigint`

   Number of `fsync` calls. These are only tracked in `context` `normal`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fsync_time `double precision`

   Time spent waiting for fsync operations in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled and `object` is not `wal`, or if [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) is enabled and `object` is `wal`, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_io View

Some backend types never perform I/O operations on some I/O objects and/or in some I/O contexts. These rows are omitted from the view. For example, the checkpointer does not checkpoint temporary tables, so there will be no rows for `backend_type` `checkpointer` and `object` `temp relation`.

In addition, some I/O operations will never be performed either by certain backend types or on certain I/O objects and/or in certain I/O contexts. These cells will be NULL. For example, temporary tables are not `fsync`ed, so `fsyncs` will be NULL for `object` `temp relation`. Also, the background writer does not perform reads, so `reads` will be NULL in rows for `backend_type` `background writer`.

For the `object` `wal`, `fsyncs` and `fsync_time` track the fsync activity of WAL files done in `issue_xlog_fsync`. `writes` and `write_time` track the write activity of WAL files done in `XLogWrite`. See [WAL Configuration](braised:ref/wal-configuration) for more information.

pg_stat_io can be used to inform database tuning. For example:

-   A high `evictions` count can indicate that shared buffers should be increased.

-   Client backends rely on the checkpointer to ensure data is persisted to permanent storage. Large numbers of `fsyncs` by `client backend`s could indicate a misconfiguration of shared buffers or of the checkpointer. More information on configuring the checkpointer can be found in [WAL Configuration](braised:ref/wal-configuration).

-   Normally, client backends should be able to rely on auxiliary processes like the checkpointer and the background writer to write out dirty data as much as possible. Large numbers of writes by client backends could indicate a misconfiguration of shared buffers or of the checkpointer. More information on configuring the checkpointer can be found in [WAL Configuration](braised:ref/wal-configuration).

:::{.callout type="note"}
Columns tracking I/O wait time will only be non-zero when [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled. The user should be careful when referencing these columns in combination with their corresponding I/O operations in case `track_io_timing` was not enabled for the entire time since the last stats reset.
:::

### pg_stat_bgwriter

The pg_stat_bgwriter view will always have a single row, containing data about the background writer of the cluster.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   buffers_clean `bigint`

   Number of buffers written by the background writer
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   maxwritten_clean `bigint`

   Number of times the background writer stopped a cleaning scan because it had written too many buffers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   buffers_alloc `bigint`

   Number of buffers allocated
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_bgwriter View

### pg_stat_checkpointer

The pg_stat_checkpointer view will always have a single row, containing data about the checkpointer process of the cluster.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   num_timed `bigint`

   Number of scheduled checkpoints due to timeout
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   num_requested `bigint`

   Number of requested checkpoints
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   num_done `bigint`

   Number of checkpoints that have been performed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   restartpoints_timed `bigint`

   Number of scheduled restartpoints due to timeout or after a failed attempt to perform it
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   restartpoints_req `bigint`

   Number of requested restartpoints
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   restartpoints_done `bigint`

   Number of restartpoints that have been performed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   write_time `double precision`

   Total amount of time that has been spent in the portion of processing checkpoints and restartpoints where files are written to disk, in milliseconds
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sync_time `double precision`

   Total amount of time that has been spent in the portion of processing checkpoints and restartpoints where files are synchronized to disk, in milliseconds
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   buffers_written `bigint`

   Number of shared buffers written during checkpoints and restartpoints
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   slru_written `bigint`

   Number of SLRU buffers written during checkpoints and restartpoints
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_checkpointer View

Checkpoints may be skipped if the server has been idle since the last one. num_timed and num_requested count both completed and skipped checkpoints, while num_done tracks only the completed ones. Similarly, restartpoints may be skipped if the last replayed checkpoint record is already the last restartpoint. restartpoints_timed and restartpoints_req count both completed and skipped restartpoints, while restartpoints_done tracks only the completed ones.

### pg_stat_wal

The pg_stat_wal view will always have a single row, containing data about WAL activity of the cluster.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_records `bigint`

   Total number of WAL records generated
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_fpi `bigint`

   Total number of WAL full page images generated
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_bytes `numeric`

   Total amount of WAL generated in bytes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_buffers_full `bigint`

   Number of times WAL data was written to disk because WAL buffers became full
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_wal View

### pg_stat_database

The pg_stat_database view will contain one row for each database in the cluster, plus one for shared objects, showing database-wide statistics.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datid `oid`

   OID of this database, or 0 for objects belonging to a shared relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datname `name`

   Name of this database, or `NULL` for shared objects.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numbackends `integer`

   Number of backends currently connected to this database, or `NULL` for shared objects. This is the only column in this view that returns a value reflecting current state; all other columns return the accumulated values since the last reset.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   xact_commit `bigint`

   Number of transactions in this database that have been committed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   xact_rollback `bigint`

   Number of transactions in this database that have been rolled back
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_read `bigint`

   Number of disk blocks read in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_hit `bigint`

   Number of times disk blocks were found already in the buffer cache, so that a read was not necessary (this only includes hits in the PostgreSQL buffer cache, not the operating system\'s file system cache)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tup_returned `bigint`

   Number of live rows fetched by sequential scans and index entries returned by index scans in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tup_fetched `bigint`

   Number of live rows fetched by index scans in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tup_inserted `bigint`

   Number of rows inserted by queries in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tup_updated `bigint`

   Number of rows updated by queries in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tup_deleted `bigint`

   Number of rows deleted by queries in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conflicts `bigint`

   Number of queries canceled due to conflicts with recovery in this database. (Conflicts occur only on standby servers; see [pg_stat_database_conflicts](#monitoring-pg-stat-database-conflicts-view) for details.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   temp_files `bigint`

   Number of temporary files created by queries in this database. All temporary files are counted, regardless of why the temporary file was created (e.g., sorting or hashing), and regardless of the [log_temp_files (integer)
      
       log_temp_files configuration parameter](braised:ref/runtime-config-logging#log-temp-files-integer-log-temp-files-configuration-parameter) setting.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   temp_bytes `bigint`

   Total amount of data written to temporary files by queries in this database. All temporary files are counted, regardless of why the temporary file was created, and regardless of the [log_temp_files (integer)
      
       log_temp_files configuration parameter](braised:ref/runtime-config-logging#log-temp-files-integer-log-temp-files-configuration-parameter) setting.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   deadlocks `bigint`

   Number of deadlocks detected in this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   checksum_failures `bigint`

   Number of data page checksum failures detected in this database (or on a shared object), or NULL if data checksums are disabled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   checksum_last_failure `timestamp with time zone`

   Time at which the last data page checksum failure was detected in this database (or on a shared object), or NULL if data checksums are disabled.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blk_read_time `double precision`

   Time spent reading data file blocks by backends in this database, in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blk_write_time `double precision`

   Time spent writing data file blocks by backends in this database, in milliseconds (if [track_io_timing (boolean)
      
       track_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-io-timing-boolean-track-io-timing-configuration-parameter) is enabled, otherwise zero)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   session_time `double precision`

   Time spent by database sessions in this database, in milliseconds (note that statistics are only updated when the state of a session changes, so if sessions have been idle for a long time, this idle time won\'t be included)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   active_time `double precision`

   Time spent executing SQL statements in this database, in milliseconds (this corresponds to the states `active` and `fastpath function call` in [pg_stat_activity](#monitoring-pg-stat-activity-view))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idle_in_transaction_time `double precision`

   Time spent idling while in a transaction in this database, in milliseconds (this corresponds to the states `idle in transaction` and `idle in transaction (aborted)` in [pg_stat_activity](#monitoring-pg-stat-activity-view))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sessions `bigint`

   Total number of sessions established to this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sessions_abandoned `bigint`

   Number of database sessions to this database that were terminated because connection to the client was lost
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sessions_fatal `bigint`

   Number of database sessions to this database that were terminated by fatal errors
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sessions_killed `bigint`

   Number of database sessions to this database that were terminated by operator intervention
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parallel_workers_to_launch `bigint`

   Number of parallel workers planned to be launched by queries on this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parallel_workers_launched `bigint`

   Number of parallel workers launched by queries on this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_database View

### pg_stat_database_conflicts

The pg_stat_database_conflicts view will contain one row per database, showing database-wide statistics about query cancels occurring due to conflicts with recovery on standby servers. This view will only contain information on standby servers, since conflicts do not occur on primary servers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datid `oid`

   OID of a database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datname `name`

   Name of this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_tablespace `bigint`

   Number of queries in this database that have been canceled due to dropped tablespaces
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_lock `bigint`

   Number of queries in this database that have been canceled due to lock timeouts
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_snapshot `bigint`

   Number of queries in this database that have been canceled due to old snapshots
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_bufferpin `bigint`

   Number of queries in this database that have been canceled due to pinned buffers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_deadlock `bigint`

   Number of queries in this database that have been canceled due to deadlocks
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confl_active_logicalslot `bigint`

   Number of uses of logical slots in this database that have been canceled due to old snapshots or too low a [wal_level (enum)
      
       wal_level configuration parameter](braised:ref/runtime-config-wal#wal-level-enum-wal-level-configuration-parameter) on the primary
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_database_conflicts View

### pg_stat_all_tables

The pg_stat_all_tables view will contain one row for each table in the current database (including TOAST tables), showing statistics about accesses to that specific table. The pg_stat_user_tables and pg_stat_sys_tables views contain the same information, but filtered to only show user and system tables respectively.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of a table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema that this table is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relname `name`

   Name of this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seq_scan `bigint`

   Number of sequential scans initiated on this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_seq_scan `timestamp with time zone`

   The time of the last sequential scan on this table, based on the most recent transaction stop time
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seq_tup_read `bigint`

   Number of live rows fetched by sequential scans
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_scan `bigint`

   Number of index scans initiated on this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_idx_scan `timestamp with time zone`

   The time of the last index scan on this table, based on the most recent transaction stop time
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_tup_fetch `bigint`

   Number of live rows fetched by index scans
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_tup_ins `bigint`

   Total number of rows inserted
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_tup_upd `bigint`

   Total number of rows updated. (This includes row updates counted in n_tup_hot_upd and n_tup_newpage_upd, and remaining non-HOT updates.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_tup_del `bigint`

   Total number of rows deleted
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_tup_hot_upd `bigint`

   Number of rows [HOT updated](#storage-hot). These are updates where no successor versions are required in indexes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_tup_newpage_upd `bigint`

   Number of rows updated where the successor version goes onto a *new* heap page, leaving behind an original version with a [t_ctid field](#storage-tuple-layout) that points to a different heap page. These are always non-HOT updates.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_live_tup `bigint`

   Estimated number of live rows
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_dead_tup `bigint`

   Estimated number of dead rows
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_mod_since_analyze `bigint`

   Estimated number of rows modified since this table was last analyzed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_ins_since_vacuum `bigint`

   Estimated number of rows inserted since this table was last vacuumed (not counting `VACUUM FULL`)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_vacuum `timestamp with time zone`

   Last time at which this table was manually vacuumed (not counting `VACUUM FULL`)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_autovacuum `timestamp with time zone`

   Last time at which this table was vacuumed by the autovacuum daemon
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_analyze `timestamp with time zone`

   Last time at which this table was manually analyzed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_autoanalyze `timestamp with time zone`

   Last time at which this table was analyzed by the autovacuum daemon
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   vacuum_count `bigint`

   Number of times this table has been manually vacuumed (not counting `VACUUM FULL`)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   autovacuum_count `bigint`

   Number of times this table has been vacuumed by the autovacuum daemon
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   analyze_count `bigint`

   Number of times this table has been manually analyzed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   autoanalyze_count `bigint`

   Number of times this table has been analyzed by the autovacuum daemon
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_vacuum_time `double precision`

   Total time this table has been manually vacuumed, in milliseconds (not counting `VACUUM FULL`). (This includes the time spent sleeping due to cost-based delays.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_autovacuum_time `double precision`

   Total time this table has been vacuumed by the autovacuum daemon, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_analyze_time `double precision`

   Total time this table has been manually analyzed, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_autoanalyze_time `double precision`

   Total time this table has been analyzed by the autovacuum daemon, in milliseconds. (This includes the time spent sleeping due to cost-based delays.)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_all_tables View

### pg_stat_all_indexes

The pg_stat_all_indexes view will contain one row for each index in the current database, showing statistics about accesses to that specific index. The pg_stat_user_indexes and pg_stat_sys_indexes views contain the same information, but filtered to only show user and system indexes respectively.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of the table for this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexrelid `oid`

   OID of this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema this index is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relname `name`

   Name of the table for this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexrelname `name`

   Name of this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_scan `bigint`

   Number of index scans initiated on this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_idx_scan `timestamp with time zone`

   The time of the last scan on this index, based on the most recent transaction stop time
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_tup_read `bigint`

   Number of index entries returned by scans on this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_tup_fetch `bigint`

   Number of live table rows fetched by simple index scans using this index
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_all_indexes View

Indexes can be used by simple index scans, "bitmap" index scans, and the optimizer. In a bitmap scan the output of several indexes can be combined via AND or OR rules, so it is difficult to associate individual heap row fetches with specific indexes when a bitmap scan is used. Therefore, a bitmap scan increments the pg_stat_all_indexes.idx_tup_read count(s) for the index(es) it uses, and it increments the pg_stat_all_tables.idx_tup_fetch count for the table, but it does not affect pg_stat_all_indexes.idx_tup_fetch. The optimizer also accesses indexes to check for supplied constants whose values are outside the recorded range of the optimizer statistics because the optimizer statistics might be stale.

:::{.callout type="note"}
The idx_tup_read and idx_tup_fetch counts can be different even without any use of bitmap scans, because idx_tup_read counts index entries retrieved from the index while idx_tup_fetch counts live rows fetched from the table. The latter will be less if any dead or not-yet-committed rows are fetched using the index, or if any heap fetches are avoided by means of an index-only scan.
:::

:::{.callout type="note"}
Index scans may sometimes perform multiple index searches per execution. Each index search increments pg_stat_all_indexes.idx_scan, so it\'s possible for the count of index scans to significantly exceed the total number of index scan executor node executions.

This can happen with queries that use certain SQL constructs to search for rows matching any value out of a list or array of multiple scalar values (see [Row and Array Comparisons](braised:ref/functions-comparisons)). It can also happen to queries with a `column_name = value1 OR column_name = value2 ...` construct, though only when the optimizer transforms the construct into an equivalent multi-valued array representation. Similarly, when B-tree index scans use the skip scan optimization, an index search is performed each time the scan is repositioned to the next index leaf page that might have matching tuples (see [Multicolumn Indexes](braised:ref/indexes-multicolumn)).
:::

:::{.callout type="tip"}
`EXPLAIN ANALYZE` outputs the total number of index searches performed by each index scan node. See [EXPLAIN ANALYZE](braised:ref/using-explain#explain-analyze) for an example demonstrating how this works.
:::

### pg_statio_all_tables

The pg_statio_all_tables view will contain one row for each table in the current database (including TOAST tables), showing statistics about I/O on that specific table.
The pg_statio_user_tables and pg_statio_sys_tables views contain the same information, but filtered to only show user and system tables respectively.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of a table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema that this table is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relname `name`

   Name of this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   heap_blks_read `bigint`

   Number of disk blocks read from this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   heap_blks_hit `bigint`

   Number of buffer hits in this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_blks_read `bigint`

   Number of disk blocks read from all indexes on this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_blks_hit `bigint`

   Number of buffer hits in all indexes on this table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   toast_blks_read `bigint`

   Number of disk blocks read from this table\'s TOAST table (if any)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   toast_blks_hit `bigint`

   Number of buffer hits in this table\'s TOAST table (if any)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tidx_blks_read `bigint`

   Number of disk blocks read from this table\'s TOAST table indexes (if any)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tidx_blks_hit `bigint`

   Number of buffer hits in this table\'s TOAST table indexes (if any)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_statio_all_tables View

### pg_statio_all_indexes

The pg_statio_all_indexes view will contain one row for each index in the current database, showing statistics about I/O on that specific index. The pg_statio_user_indexes and pg_statio_sys_indexes views contain the same information, but filtered to only show user and system indexes respectively.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of the table for this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexrelid `oid`

   OID of this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema this index is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relname `name`

   Name of the table for this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexrelname `name`

   Name of this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_blks_read `bigint`

   Number of disk blocks read from this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   idx_blks_hit `bigint`

   Number of buffer hits in this index
  :::{/cell}
  :::{/row}
:::{/table}

: pg_statio_all_indexes View

### pg_statio_all_sequences

The pg_statio_all_sequences view will contain one row for each sequence in the current database, showing statistics about I/O on that specific sequence.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relid `oid`

   OID of a sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema this sequence is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relname `name`

   Name of this sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_read `bigint`

   Number of disk blocks read from this sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_hit `bigint`

   Number of buffer hits in this sequence
  :::{/cell}
  :::{/row}
:::{/table}

: pg_statio_all_sequences View

### pg_stat_user_functions

The pg_stat_user_functions view will contain one row for each tracked function, showing statistics about executions of that function. The [track_functions (enum)
      
       track_functions configuration parameter](braised:ref/runtime-config-statistics#track-functions-enum-track-functions-configuration-parameter) parameter controls exactly which functions are tracked.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   funcid `oid`

   OID of a function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name`

   Name of the schema this function is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   funcname `name`

   Name of this function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   calls `bigint`

   Number of times this function has been called
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_time `double precision`

   Total time spent in this function and all other functions called by it, in milliseconds
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   self_time `double precision`

   Total time spent in this function itself, not including other functions called by it, in milliseconds
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_user_functions View

### pg_stat_slru

PostgreSQL accesses certain on-disk information via `SLRU` (simple least-recently-used) caches. The pg_stat_slru view will contain one row for each tracked SLRU cache, showing statistics about access to cached pages.

For each `SLRU` cache that\'s part of the core server, there is a configuration parameter that controls its size, with the suffix `_buffers` appended.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `text`

   Name of the SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_zeroed `bigint`

   Number of blocks zeroed during initializations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_hit `bigint`

   Number of times disk blocks were found already in the SLRU, so that a read was not necessary (this only includes hits in the SLRU, not the operating system\'s file system cache)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_read `bigint`

   Number of disk blocks read for this SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_written `bigint`

   Number of disk blocks written for this SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   blks_exists `bigint`

   Number of blocks checked for existence for this SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   flushes `bigint`

   Number of flushes of dirty data for this SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   truncates `bigint`

   Number of truncates for this SLRU
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stats_reset `timestamp with time zone`

   Time at which these statistics were last reset
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stat_slru View

### Statistics Functions

Other ways of looking at the statistics can be set up by writing queries that use the same underlying statistics access functions used by the standard views shown above. For details such as the functions\' names, consult the definitions of the standard views. (For example, in psql you could issue `\d+ pg_stat_activity`.) The access functions for per-database statistics take a database OID as an argument to identify which database to report on. The per-table and per-index functions take a table or index OID. The functions for per-function statistics take a function OID. Note that only tables, indexes, and functions in the current database can be seen with these functions.

Additional functions related to the cumulative statistics system are listed in Additional Statistics Functions.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_backend_pid` () integer

   Returns the process ID of the server process attached to the current session.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_io` ( `integer` ) setof record

   Returns I/O statistics about the backend with the specified process ID. The output fields are exactly the same as the ones in the pg_stat_io view.

   The function does not return I/O statistics for the checkpointer, the background writer, the startup process and the autovacuum launcher as they are already visible in the pg_stat_io view and there is only one of each.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_activity` ( `integer` ) setof record

   Returns a record of information about the backend with the specified process ID, or one record for each active backend in the system if `NULL` is specified. The fields returned are a subset of those in the pg_stat_activity view.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_wal` ( `integer` ) record

   Returns WAL statistics about the backend with the specified process ID. The output fields are exactly the same as the ones in the pg_stat_wal view.

   The function does not return WAL statistics for the checkpointer, the background writer, the startup process and the autovacuum launcher.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_snapshot_timestamp` () timestamp with time zone

   Returns the timestamp of the current statistics snapshot, or NULL if no statistics snapshot has been taken. A snapshot is taken the first time cumulative statistics are accessed in a transaction if `stats_fetch_consistency` is set to `snapshot`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_xact_blocks_fetched` ( `oid` ) bigint

   Returns the number of block read requests for table or index, in the current transaction. This number minus `pg_stat_get_xact_blocks_hit` gives the number of kernel `read()` calls; the number of actual physical reads is usually lower due to kernel-level buffering.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_xact_blocks_hit` ( `oid` ) bigint

   Returns the number of block read requests for table or index, in the current transaction, found in cache (not triggering kernel `read()` calls).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_clear_snapshot` () void

   Discards the current statistics snapshot or cached information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset` () void

   Resets all statistics counters for the current database to zero.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_shared` ( \[ `target` `text` `DEFAULT` `NULL` \] ) void

   Resets some cluster-wide statistics counters to zero, depending on the argument. `target` can be:

   -   `archiver`: Reset all the counters shown in the pg_stat_archiver view.

   -   `bgwriter`: Reset all the counters shown in the pg_stat_bgwriter view.

   -   `checkpointer`: Reset all the counters shown in the pg_stat_checkpointer view.

   -   `io`: Reset all the counters shown in the pg_stat_io view.

   -   `recovery_prefetch`: Reset all the counters shown in the pg_stat_recovery_prefetch view.

   -   `slru`: Reset all the counters shown in the pg_stat_slru view.

   -   `wal`: Reset all the counters shown in the pg_stat_wal view.

   -   `NULL` or not specified: All the counters from the views listed above are reset.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_single_table_counters` ( `oid` ) void

   Resets statistics for a single table or index in the current database or shared across all databases in the cluster to zero.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_backend_stats` ( `integer` ) void

   Resets statistics for a single backend with the specified process ID to zero.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_single_function_counters` ( `oid` ) void

   Resets statistics for a single function in the current database to zero.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_slru` ( \[ `target` `text` `DEFAULT` `NULL` \] ) void

   Resets statistics to zero for a single SLRU cache, or for all SLRUs in the cluster. If `target` is `NULL` or is not specified, all the counters shown in the pg_stat_slru view for all SLRU caches are reset. The argument can be one of `commit_timestamp`, `multixact_member`, `multixact_offset`, `notify`, `serializable`, `subtransaction`, or `transaction` to reset the counters for only that entry. If the argument is `other` (or indeed, any unrecognized name), then the counters for all other SLRU caches, such as extension-defined caches, are reset.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_replication_slot` ( `text` ) void

   Resets statistics of the replication slot defined by the argument. If the argument is `NULL`, resets statistics for all the replication slots.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_reset_subscription_stats` ( `oid` ) void

   Resets statistics for a single subscription shown in the pg_stat_subscription_stats view to zero. If the argument is `NULL`, reset statistics for all subscriptions.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
:::{/table}

: Additional Statistics Functions

:::{.callout type="warning"}
Using `pg_stat_reset()` also resets counters that autovacuum uses to determine when to trigger a vacuum or an analyze. Resetting these counters can cause autovacuum to not perform necessary work, which can cause problems such as table bloat or out-dated table statistics. A database-wide `ANALYZE` is recommended after the statistics have been reset.
:::

`pg_stat_get_activity`, the underlying function of the pg_stat_activity view, returns a set of records containing all the available information about each backend process.
Sometimes it may be more convenient to obtain just a subset of this information.
In such cases, another set of per-backend statistics access functions can be used; these are shown in Per-Backend Statistics Functions.
These access functions use the session\'s backend ID number, which is a small integer (\>= 0) that is distinct from the backend ID of any concurrent session, although a session\'s ID can be recycled as soon as it exits.
The backend ID is used, among other things, to identify the session\'s temporary schema if it has one.
The function `pg_stat_get_backend_idset` provides a convenient way to list all the active backends\' ID numbers for invoking these functions.
For example, to show the PIDs and current queries of all backends:

    SELECT pg_stat_get_backend_pid(backendid) AS pid,
           pg_stat_get_backend_activity(backendid) AS query
    FROM pg_stat_get_backend_idset() AS backendid;

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_activity` ( `integer` ) text

   Returns the text of this backend\'s most recent query.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_activity_start` ( `integer` ) timestamp with time zone

   Returns the time when the backend\'s most recent query was started.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_client_addr` ( `integer` ) inet

   Returns the IP address of the client connected to this backend.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_client_port` ( `integer` ) integer

   Returns the TCP port number that the client is using for communication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_dbid` ( `integer` ) oid

   Returns the OID of the database this backend is connected to.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_idset` () setof integer

   Returns the set of currently active backend ID numbers.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_pid` ( `integer` ) integer

   Returns the process ID of this backend.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_start` ( `integer` ) timestamp with time zone

   Returns the time when this process was started.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_subxact` ( `integer` ) record

   Returns a record of information about the subtransactions of the backend with the specified ID. The fields returned are `subxact_count`, which is the number of subtransactions in the backend\'s subtransaction cache, and `subxact_overflow`, which indicates whether the backend\'s subtransaction cache is overflowed or not.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_userid` ( `integer` ) oid

   Returns the OID of the user logged into this backend.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_wait_event` ( `integer` ) text

   Returns the wait event name if this backend is currently waiting, otherwise NULL. See Wait Events of Type  through Wait Events of Type .
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_wait_event_type` ( `integer` ) text

   Returns the wait event type name if this backend is currently waiting, otherwise NULL. See Wait Event Types for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_get_backend_xact_start` ( `integer` ) timestamp with time zone

   Returns the time when the backend\'s current transaction was started.
  :::{/cell}
  :::{/row}
:::{/table}

: Per-Backend Statistics Functions
