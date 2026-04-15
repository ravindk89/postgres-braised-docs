---
title: "9.28. System Administration Functions"
id: functions-admin
---

## System Administration Functions

The functions described in this section are used to control and monitor a PostgreSQL installation.

### Configuration Settings Functions

Configuration Settings Functions shows the functions available to query and alter run-time configuration parameters.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description

   Example(s)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `current_setting` ( `setting_name` `text` \[, `missing_ok` `boolean`\] ) text

   Returns the current value of the setting `setting_name`. If there is no such setting, `current_setting` throws an error unless `missing_ok` is supplied and is `true` (in which case NULL is returned). This function corresponds to the SQL command [SHOW](braised:ref/sql-show).

   `current_setting('datestyle')` ISO, MDY
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `set_config` ( `setting_name` `text`, `new_value` `text`, `is_local` `boolean` ) text

   Sets the parameter `setting_name` to `new_value`, and returns that value. If `is_local` is `true`, the new value will only apply during the current transaction. If you want the new value to apply for the rest of the current session, use `false` instead. This function corresponds to the SQL command [SET](braised:ref/sql-set).

   `set_config` accepts the NULL value for `new_value`, but as settings cannot be null, it is interpreted as a request to reset the setting to its default value.

   `set_config('log_statement_stats', 'off', false)` off
  :::{/cell}
  :::{/row}
:::{/table}

: Configuration Settings Functions

### Server Signaling Functions

The functions shown in Server Signaling Functions send control signals to other server processes. Use of these functions is restricted to superusers by default but access may be granted to others using `GRANT`, with noted exceptions.

Each of these functions returns `true` if the signal was successfully sent and `false` if sending the signal failed.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_cancel_backend` ( `pid` `integer` ) boolean

   Cancels the current query of the session whose backend process has the specified process ID. This is also allowed if the calling role is a member of the role whose backend is being canceled or the calling role has privileges of `pg_signal_backend`, however only superusers can cancel superuser backends. As an exception, roles with privileges of `pg_signal_autovacuum_worker` are permitted to cancel autovacuum worker processes, which are otherwise considered superuser backends.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_log_backend_memory_contexts` ( `pid` `integer` ) boolean

   Requests to log the memory contexts of the backend with the specified process ID. This function can send the request to backends and auxiliary processes except logger. These memory contexts will be logged at `LOG` message level. They will appear in the server log based on the log configuration set (see [Error Reporting and Logging](braised:ref/runtime-config-logging) for more information), but will not be sent to the client regardless of [client_min_messages (enum)
      
       client_min_messages configuration parameter](braised:ref/runtime-config-client#client-min-messages-enum-client-min-messages-configuration-parameter).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_reload_conf` () boolean

   Causes all processes of the PostgreSQL server to reload their configuration files. (This is initiated by sending a `SIGHUP` signal to the postmaster process, which in turn sends `SIGHUP` to each of its children.) You can use the [pg_file_settings](#view-pg-file-settings), [pg_hba_file_rules](#view-pg-hba-file-rules) and [pg_ident_file_mappings](#view-pg-ident-file-mappings) views to check the configuration files for possible errors, before reloading.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_rotate_logfile` () boolean

   Signals the log-file manager to switch to a new output file immediately. This works only when the built-in log collector is running, since otherwise there is no log-file manager subprocess.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_terminate_backend` ( `pid` `integer`, `timeout` `bigint` `DEFAULT` `0` ) boolean

   Terminates the session whose backend process has the specified process ID. This is also allowed if the calling role is a member of the role whose backend is being terminated or the calling role has privileges of `pg_signal_backend`, however only superusers can terminate superuser backends. As an exception, roles with privileges of `pg_signal_autovacuum_worker` are permitted to terminate autovacuum worker processes, which are otherwise considered superuser backends.

   If `timeout` is not specified or zero, this function returns `true` whether the process actually terminates or not, indicating only that the sending of the signal was successful. If the `timeout` is specified (in milliseconds) and greater than zero, the function waits until the process is actually terminated or until the given time has passed. If the process is terminated, the function returns `true`. On timeout, a warning is emitted and `false` is returned.
  :::{/cell}
  :::{/row}
:::{/table}

: Server Signaling Functions

`pg_cancel_backend` and `pg_terminate_backend` send signals (`SIGINT` or `SIGTERM` respectively) to backend processes identified by process ID. The process ID of an active backend can be found from the pid column of the pg_stat_activity view, or by listing the `postgres` processes on the server (using ps on Unix or the Task Manager on Windows). The role of an active backend can be found from the usename column of the pg_stat_activity view.

`pg_log_backend_memory_contexts` can be used to log the memory contexts of a backend process. For example:

    postgres=# SELECT pg_log_backend_memory_contexts(pg_backend_pid());
     pg_log_backend_memory_contexts
    --------------------------------
     t
    (1 row)

One message for each memory context will be logged. For example:

    LOG:  logging memory contexts of PID 10377
    STATEMENT:  SELECT pg_log_backend_memory_contexts(pg_backend_pid());
    LOG:  level: 1; TopMemoryContext: 80800 total in 6 blocks; 14432 free (5 chunks); 66368 used
    LOG:  level: 2; pgstat TabStatusArray lookup hash table: 8192 total in 1 blocks; 1408 free (0 chunks); 6784 used
    LOG:  level: 2; TopTransactionContext: 8192 total in 1 blocks; 7720 free (1 chunks); 472 used
    LOG:  level: 2; RowDescriptionContext: 8192 total in 1 blocks; 6880 free (0 chunks); 1312 used
    LOG:  level: 2; MessageContext: 16384 total in 2 blocks; 5152 free (0 chunks); 11232 used
    LOG:  level: 2; Operator class cache: 8192 total in 1 blocks; 512 free (0 chunks); 7680 used
    LOG:  level: 2; smgr relation table: 16384 total in 2 blocks; 4544 free (3 chunks); 11840 used
    LOG:  level: 2; TransactionAbortContext: 32768 total in 1 blocks; 32504 free (0 chunks); 264 used
    ...
    LOG:  level: 2; ErrorContext: 8192 total in 1 blocks; 7928 free (3 chunks); 264 used
    LOG:  Grand total: 1651920 bytes in 201 blocks; 622360 free (88 chunks); 1029560 used

If there are more than 100 child contexts under the same parent, the first 100 child contexts are logged, along with a summary of the remaining contexts. Note that frequent calls to this function could incur significant overhead, because it may generate a large number of log messages.

### Backup Control Functions

The functions shown in Backup Control Functions assist in making on-line backups. These functions cannot be executed during recovery (except `pg_backup_start`, `pg_backup_stop`, and `pg_wal_lsn_diff`).

For details about proper usage of these functions, see [Continuous Archiving and Point-in-Time Recovery (PITR)](braised:ref/continuous-archiving).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_create_restore_point` ( `name` `text` ) pg_lsn

   Creates a named marker record in the write-ahead log that can later be used as a recovery target, and returns the corresponding write-ahead log location. The given name can then be used with [recovery_target_name (string)
      
        recovery_target_name configuration parameter](braised:ref/runtime-config-wal#recovery-target-name-string-recovery-target-name-configuration-parameter) to specify the point up to which recovery will proceed. Avoid creating multiple restore points with the same name, since recovery will stop at the first one whose name matches the recovery target.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_current_wal_flush_lsn` () pg_lsn

   Returns the current write-ahead log flush location (see notes below).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_current_wal_insert_lsn` () pg_lsn

   Returns the current write-ahead log insert location (see notes below).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_current_wal_lsn` () pg_lsn

   Returns the current write-ahead log write location (see notes below).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_backup_start` ( `label` `text` \[, `fast` `boolean`\] ) pg_lsn

   Prepares the server to begin an on-line backup. The only required parameter is an arbitrary user-defined label for the backup. (Typically this would be the name under which the backup dump file will be stored.) If the optional second parameter is given as `true`, it specifies executing `pg_backup_start` as quickly as possible. This forces an immediate checkpoint which will cause a spike in I/O operations, slowing any concurrently executing queries.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_backup_stop` ( \[`wait_for_archive` `boolean`\] ) record ( `lsn` `pg_lsn`, `labelfile` `text`, `spcmapfile` `text` )

   Finishes performing an on-line backup. The desired contents of the backup label file and the tablespace map file are returned as part of the result of the function and must be written to files in the backup area. These files must not be written to the live data directory (doing so will cause PostgreSQL to fail to restart in the event of a crash).

   There is an optional parameter of type `boolean`. If false, the function will return immediately after the backup is completed, without waiting for WAL to be archived. This behavior is only useful with backup software that independently monitors WAL archiving. Otherwise, WAL required to make the backup consistent might be missing and make the backup useless. By default or when this parameter is true, `pg_backup_stop` will wait for WAL to be archived when archiving is enabled. (On a standby, this means that it will wait only when `archive_mode` = `always`. If write activity on the primary is low, it may be useful to run `pg_switch_wal` on the primary in order to trigger an immediate segment switch.)

   When executed on a primary, this function also creates a backup history file in the write-ahead log archive area. The history file includes the label given to `pg_backup_start`, the starting and ending write-ahead log locations for the backup, and the starting and ending times of the backup. After recording the ending location, the current write-ahead log insertion point is automatically advanced to the next write-ahead log file, so that the ending write-ahead log file can be archived immediately to complete the backup.

   The result of the function is a single record. The `lsn` column holds the backup\'s ending write-ahead log location (which again can be ignored). The second column returns the contents of the backup label file, and the third column returns the contents of the tablespace map file. These must be stored as part of the backup and are required as part of the restore process.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_switch_wal` () pg_lsn

   Forces the server to switch to a new write-ahead log file, which allows the current file to be archived (assuming you are using continuous archiving). The result is the ending write-ahead log location plus 1 within the just-completed write-ahead log file. If there has been no write-ahead log activity since the last write-ahead log switch, `pg_switch_wal` does nothing and returns the start location of the write-ahead log file currently in use.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_walfile_name` ( `lsn` `pg_lsn` ) text

   Converts a write-ahead log location to the name of the WAL file holding that location.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_walfile_name_offset` ( `lsn` `pg_lsn` ) record ( `file_name` `text`, `file_offset` `integer` )

   Converts a write-ahead log location to a WAL file name and byte offset within that file.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_split_walfile_name` ( `file_name` `text` ) record ( `segment_number` `numeric`, `timeline_id` `bigint` )

   Extracts the sequence number and timeline ID from a WAL file name.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_wal_lsn_diff` ( `lsn1` `pg_lsn`, `lsn2` `pg_lsn` ) numeric

   Calculates the difference in bytes (`lsn1` - `lsn2`) between two write-ahead log locations. This can be used with pg_stat_replication or some of the functions shown in Backup Control Functions to get the replication lag.
  :::{/cell}
  :::{/row}
:::{/table}

: Backup Control Functions

`pg_current_wal_lsn` displays the current write-ahead log write location in the same format used by the above functions. Similarly, `pg_current_wal_insert_lsn` displays the current write-ahead log insertion location and `pg_current_wal_flush_lsn` displays the current write-ahead log flush location. The insertion location is the "logical" end of the write-ahead log at any instant, while the write location is the end of what has actually been written out from the server\'s internal buffers, and the flush location is the last location known to be written to durable storage. The write location is the end of what can be examined from outside the server, and is usually what you want if you are interested in archiving partially-complete write-ahead log files. The insertion and flush locations are made available primarily for server debugging purposes. These are all read-only operations and do not require superuser permissions.

You can use `pg_walfile_name_offset` to extract the corresponding write-ahead log file name and byte offset from a `pg_lsn` value. For example:

    postgres=# SELECT * FROM pg_walfile_name_offset((pg_backup_stop()).lsn);
            file_name         | file_offset
    --------------------------+-------------
     00000001000000000000000D |     4039624
    (1 row)

Similarly, `pg_walfile_name` extracts just the write-ahead log file name.

`pg_split_walfile_name` is useful to compute a LSN from a file offset and WAL file name, for example:

    postgres=# \set file_name '000000010000000100C000AB'
    postgres=# \set offset 256
    postgres=# SELECT '0/0'::pg_lsn + pd.segment_number * ps.setting::int + :offset AS lsn
      FROM pg_split_walfile_name(:'file_name') pd,
           pg_show_all_settings() ps
      WHERE ps.name = 'wal_segment_size';
          lsn
    ---------------
     C001/AB000100
    (1 row)

### Recovery Control Functions

The functions shown in Recovery Information Functions provide information about the current status of a standby server. These functions may be executed both during recovery and in normal running.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_is_in_recovery` () boolean

   Returns true if recovery is still in progress.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_last_wal_receive_lsn` () pg_lsn

   Returns the last write-ahead log location that has been received and synced to disk by streaming replication. While streaming replication is in progress this will increase monotonically. If recovery has completed then this will remain static at the location of the last WAL record received and synced to disk during recovery. If streaming replication is disabled, or if it has not yet started, the function returns `NULL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_last_wal_replay_lsn` () pg_lsn

   Returns the last write-ahead log location that has been replayed during recovery. If recovery is still in progress this will increase monotonically. If recovery has completed then this will remain static at the location of the last WAL record applied during recovery. When the server has been started normally without recovery, the function returns `NULL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_last_xact_replay_timestamp` () timestamp with time zone

   Returns the time stamp of the last transaction replayed during recovery. This is the time at which the commit or abort WAL record for that transaction was generated on the primary. If no transactions have been replayed during recovery, the function returns `NULL`. Otherwise, if recovery is still in progress this will increase monotonically. If recovery has completed then this will remain static at the time of the last transaction applied during recovery. When the server has been started normally without recovery, the function returns `NULL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_get_wal_resource_managers` () setof record ( `rm_id` `integer`, `rm_name` `text`, `rm_builtin` `boolean` )

   Returns the currently-loaded WAL resource managers in the system. The column `rm_builtin` indicates whether it\'s a built-in resource manager, or a custom resource manager loaded by an extension.
  :::{/cell}
  :::{/row}
:::{/table}

: Recovery Information Functions

The functions shown in Recovery Control Functions control the progress of recovery. These functions may be executed only during recovery.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_is_wal_replay_paused` () boolean

   Returns true if recovery pause is requested.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_get_wal_replay_pause_state` () text

   Returns recovery pause state. The return values are `not paused` if pause is not requested, `pause requested` if pause is requested but recovery is not yet paused, and `paused` if the recovery is actually paused.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_promote` ( `wait` `boolean` `DEFAULT` `true`, `wait_seconds` `integer` `DEFAULT` `60` ) boolean

   Promotes a standby server to primary status. With `wait` set to `true` (the default), the function waits until promotion is completed or `wait_seconds` seconds have passed, and returns `true` if promotion is successful and `false` otherwise. If `wait` is set to `false`, the function returns `true` immediately after sending a `SIGUSR1` signal to the postmaster to trigger promotion.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_wal_replay_pause` () void

   Request to pause recovery. A request doesn\'t mean that recovery stops right away. If you want a guarantee that recovery is actually paused, you need to check for the recovery pause state returned by `pg_get_wal_replay_pause_state()`. Note that `pg_is_wal_replay_paused()` returns whether a request is made. While recovery is paused, no further database changes are applied. If hot standby is active, all new queries will see the same consistent snapshot of the database, and no further query conflicts will be generated until recovery is resumed.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_wal_replay_resume` () void

   Restarts recovery if it was paused.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
:::{/table}

: Recovery Control Functions

`pg_wal_replay_pause` and `pg_wal_replay_resume` cannot be executed while a promotion is ongoing. If a promotion is triggered while recovery is paused, the paused state ends and promotion continues.

If streaming replication is disabled, the paused state may continue indefinitely without a problem. If streaming replication is in progress then WAL records will continue to be received, which will eventually fill available disk space, depending upon the duration of the pause, the rate of WAL generation and available disk space.

### Snapshot Synchronization Functions

PostgreSQL allows database sessions to synchronize their snapshots. A snapshot determines which data is visible to the transaction that is using the snapshot. Synchronized snapshots are necessary when two or more sessions need to see identical content in the database. If two sessions just start their transactions independently, there is always a possibility that some third transaction commits between the executions of the two `START TRANSACTION` commands, so that one session sees the effects of that transaction and the other does not.

To solve this problem, PostgreSQL allows a transaction to export the snapshot it is using. As long as the exporting transaction remains open, other transactions can import its snapshot, and thereby be guaranteed that they see exactly the same view of the database that the first transaction sees. But note that any database changes made by any one of these transactions remain invisible to the other transactions, as is usual for changes made by uncommitted transactions. So the transactions are synchronized with respect to pre-existing data, but act normally for changes they make themselves.

Snapshots are exported with the `pg_export_snapshot` function, shown in Snapshot Synchronization Functions, and imported with the [SET TRANSACTION](braised:ref/sql-set-transaction) command.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_export_snapshot` () text

   Saves the transaction\'s current snapshot and returns a `text` string identifying the snapshot. This string must be passed (outside the database) to clients that want to import the snapshot. The snapshot is available for import only until the end of the transaction that exported it.

   A transaction can export more than one snapshot, if needed. Note that doing so is only useful in `READ COMMITTED` transactions, since in `REPEATABLE READ` and higher isolation levels, transactions use the same snapshot throughout their lifetime. Once a transaction has exported any snapshots, it cannot be prepared with [PREPARE TRANSACTION](braised:ref/sql-prepare-transaction).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_log_standby_snapshot` () pg_lsn

   Take a snapshot of running transactions and write it to WAL, without having to wait for bgwriter or checkpointer to log one. This is useful for logical decoding on standby, as logical slot creation has to wait until such a record is replayed on the standby.
  :::{/cell}
  :::{/row}
:::{/table}

: Snapshot Synchronization Functions

### Replication Management Functions

The functions shown in Replication Management Functions are for controlling and interacting with replication features. See [Streaming Replication](braised:ref/warm-standby#streaming-replication), [Replication Slots](braised:ref/warm-standby#replication-slots), and [Replication Progress Tracking](braised:ref/replication-origins) for information about the underlying features. Use of functions for replication origin is only allowed to the superuser by default, but may be allowed to other users by using the `GRANT` command. Use of functions for replication slots is restricted to superusers and users having `REPLICATION` privilege.

Many of these functions have equivalent commands in the replication protocol; see [Streaming Replication Protocol](braised:ref/protocol-replication).

The functions described in [Backup Control Functions](#functions-admin-backup), [Recovery Control Functions](#functions-recovery-control), and [Snapshot Synchronization Functions](#functions-snapshot-synchronization) are also relevant for replication.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_create_physical_replication_slot` ( `slot_name` `name` \[, `immediately_reserve` `boolean`, `temporary` `boolean`\] ) record ( `slot_name` `name`, `lsn` `pg_lsn` )

   Creates a new physical replication slot named `slot_name`. The optional second parameter, when `true`, specifies that the LSN for this replication slot be reserved immediately; otherwise the LSN is reserved on first connection from a streaming replication client. Streaming changes from a physical slot is only possible with the streaming-replication protocol see [Streaming Replication Protocol](braised:ref/protocol-replication). The optional third parameter, `temporary`, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by the current session. Temporary slots are also released upon any error. This function corresponds to the replication protocol command `CREATE_REPLICATION_SLOT ... PHYSICAL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_drop_replication_slot` ( `slot_name` `name` ) void

   Drops the physical or logical replication slot named `slot_name`. Same as replication protocol command `DROP_REPLICATION_SLOT`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_create_logical_replication_slot` ( `slot_name` `name`, `plugin` `name` \[, `temporary` `boolean`, `twophase` `boolean`, `failover` `boolean`\] ) record ( `slot_name` `name`, `lsn` `pg_lsn` )

   Creates a new logical (decoding) replication slot named `slot_name` using the output plugin `plugin`. The optional third parameter, `temporary`, when set to true, specifies that the slot should not be permanently stored to disk and is only meant for use by the current session. Temporary slots are also released upon any error. The optional fourth parameter, `twophase`, when set to true, specifies that the decoding of prepared transactions is enabled for this slot. The optional fifth parameter, `failover`, when set to true, specifies that this slot is enabled to be synced to the standbys so that logical replication can be resumed after failover. A call to this function has the same effect as the replication protocol command `CREATE_REPLICATION_SLOT ... LOGICAL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_copy_physical_replication_slot` ( `src_slot_name` `name`, `dst_slot_name` `name` \[, `temporary` `boolean`\] ) record ( `slot_name` `name`, `lsn` `pg_lsn` )

   Copies an existing physical replication slot named `src_slot_name` to a physical replication slot named `dst_slot_name`. The copied physical slot starts to reserve WAL from the same LSN as the source slot. `temporary` is optional. If `temporary` is omitted, the same value as the source slot is used. Copy of an invalidated slot is not allowed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_copy_logical_replication_slot` ( `src_slot_name` `name`, `dst_slot_name` `name` \[, `temporary` `boolean` \[, `plugin` `name`\]\] ) record ( `slot_name` `name`, `lsn` `pg_lsn` )

   Copies an existing logical replication slot named `src_slot_name` to a logical replication slot named `dst_slot_name`, optionally changing the output plugin and persistence. The copied logical slot starts from the same LSN as the source logical slot. Both `temporary` and `plugin` are optional; if they are omitted, the values of the source slot are used. The `failover` option of the source logical slot is not copied and is set to `false` by default. This is to avoid the risk of being unable to continue logical replication after failover to standby where the slot is being synchronized. Copy of an invalidated slot is not allowed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_logical_slot_get_changes` ( `slot_name` `name`, `upto_lsn` `pg_lsn`, `upto_nchanges` `integer`, `VARIADIC` `options` `text[]` ) setof record ( `lsn` `pg_lsn`, `xid` `xid`, `data` `text` )

   Returns changes in the slot `slot_name`, starting from the point from which changes have been consumed last. If `upto_lsn` and `upto_nchanges` are NULL, logical decoding will continue until end of WAL. If `upto_lsn` is non-NULL, decoding will include only those transactions which commit prior to the specified LSN. If `upto_nchanges` is non-NULL, decoding will stop when the number of rows produced by decoding exceeds the specified value. Note, however, that the actual number of rows returned may be larger, since this limit is only checked after adding the rows produced when decoding each new transaction commit. If the specified slot is a logical failover slot then the function will not return until all physical slots specified in `synchronized_standby_slots` have confirmed WAL receipt.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_logical_slot_peek_changes` ( `slot_name` `name`, `upto_lsn` `pg_lsn`, `upto_nchanges` `integer`, `VARIADIC` `options` `text[]` ) setof record ( `lsn` `pg_lsn`, `xid` `xid`, `data` `text` )

   Behaves just like the `pg_logical_slot_get_changes()` function, except that changes are not consumed; that is, they will be returned again on future calls.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_logical_slot_get_binary_changes` ( `slot_name` `name`, `upto_lsn` `pg_lsn`, `upto_nchanges` `integer`, `VARIADIC` `options` `text[]` ) setof record ( `lsn` `pg_lsn`, `xid` `xid`, `data` `bytea` )

   Behaves just like the `pg_logical_slot_get_changes()` function, except that changes are returned as `bytea`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_logical_slot_peek_binary_changes` ( `slot_name` `name`, `upto_lsn` `pg_lsn`, `upto_nchanges` `integer`, `VARIADIC` `options` `text[]` ) setof record ( `lsn` `pg_lsn`, `xid` `xid`, `data` `bytea` )

   Behaves just like the `pg_logical_slot_peek_changes()` function, except that changes are returned as `bytea`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_slot_advance` ( `slot_name` `name`, `upto_lsn` `pg_lsn` ) record ( `slot_name` `name`, `end_lsn` `pg_lsn` )

   Advances the current confirmed position of a replication slot named `slot_name`. The slot will not be moved backwards, and it will not be moved beyond the current insert location. Returns the name of the slot and the actual position that it was advanced to. The updated slot position information is written out at the next checkpoint if any advancing is done. So in the event of a crash, the slot may return to an earlier position. If the specified slot is a logical failover slot then the function will not return until all physical slots specified in `synchronized_standby_slots` have confirmed WAL receipt.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_create` ( `node_name` `text` ) oid

   Creates a replication origin with the given external name, and returns the internal ID assigned to it. The name must be no longer than 512 bytes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_drop` ( `node_name` `text` ) void

   Deletes a previously-created replication origin, including any associated replay progress.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_oid` ( `node_name` `text` ) oid

   Looks up a replication origin by name and returns the internal ID. If no such replication origin is found, `NULL` is returned.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_session_setup` ( `node_name` `text` ) void

   Marks the current session as replaying from the given origin, allowing replay progress to be tracked. Can only be used if no origin is currently selected. Use `pg_replication_origin_session_reset` to undo.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_session_reset` () void

   Cancels the effects of `pg_replication_origin_session_setup()`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_session_is_setup` () boolean

   Returns true if a replication origin has been selected in the current session.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_session_progress` ( `flush` `boolean` ) pg_lsn

   Returns the replay location for the replication origin selected in the current session. The parameter `flush` determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_xact_setup` ( `origin_lsn` `pg_lsn`, `origin_timestamp` `timestamp with time zone` ) void

   Marks the current transaction as replaying a transaction that has committed at the given LSN and timestamp. Can only be called when a replication origin has been selected using `pg_replication_origin_session_setup`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_xact_reset` () void

   Cancels the effects of `pg_replication_origin_xact_setup()`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_advance` ( `node_name` `text`, `lsn` `pg_lsn` ) void

   Sets replication progress for the given node to the given location. This is primarily useful for setting up the initial location, or setting a new location after configuration changes and similar. Be aware that careless use of this function can lead to inconsistently replicated data.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_replication_origin_progress` ( `node_name` `text`, `flush` `boolean` ) pg_lsn

   Returns the replay location for the given replication origin. The parameter `flush` determines whether the corresponding local transaction will be guaranteed to have been flushed to disk or not.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_logical_emit_message` ( `transactional` `boolean`, `prefix` `text`, `content` `text` \[, `flush` `boolean` `DEFAULT` `false`\] ) pg_lsn

   `pg_logical_emit_message` ( `transactional` `boolean`, `prefix` `text`, `content` `bytea` \[, `flush` `boolean` `DEFAULT` `false`\] ) pg_lsn

   Emits a logical decoding message. This can be used to pass generic messages to logical decoding plugins through WAL. The `transactional` parameter specifies if the message should be part of the current transaction, or if it should be written immediately and decoded as soon as the logical decoder reads the record. The `prefix` parameter is a textual prefix that can be used by logical decoding plugins to easily recognize messages that are interesting for them. The `content` parameter is the content of the message, given either in text or binary form. The `flush` parameter (default set to `false`) controls if the message is immediately flushed to WAL or not. `flush` has no effect with `transactional`, as the message\'s WAL record is flushed along with its transaction.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_sync_replication_slots` () void

   Synchronize the logical failover replication slots from the primary server to the standby server. This function can only be executed on the standby server. Temporary synced slots, if any, cannot be used for logical decoding and must be dropped after promotion. See [Replication Slot Synchronization](braised:ref/logicaldecoding-explanation#replication-slot-synchronization) for details. Note that this function is primarily intended for testing and debugging purposes and should be used with caution. Additionally, this function cannot be executed if `sync_replication_slots` is enabled and the slotsync worker is already running to perform the synchronization of slots.

   :::{.callout type="caution"}
   If, after executing the function, `hot_standby_feedback` is disabled on the standby or the physical slot configured in `primary_slot_name` is removed, then it is possible that the necessary rows of the synchronized slot will be removed by the VACUUM process on the primary server, resulting in the synchronized slot becoming invalidated.
   :::
  :::{/cell}
  :::{/row}
:::{/table}

: Replication Management Functions

### Database Object Management Functions

The functions shown in [Database Object Size Functions](#functions-admin-dbsize) calculate the disk space usage of database objects, or assist in presentation or understanding of usage results. `bigint` results are measured in bytes. If an OID that does not represent an existing object is passed to one of these functions, `NULL` is returned.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_column_size` ( `"any"` ) integer

   Shows the number of bytes used to store any individual data value. If applied directly to a table column value, this reflects any compression that was done.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_column_compression` ( `"any"` ) text

   Shows the compression algorithm that was used to compress an individual variable-length value. Returns `NULL` if the value is not compressed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_column_toast_chunk_id` ( `"any"` ) oid

   Shows the chunk_id of an on-disk TOASTed value. Returns `NULL` if the value is un-TOASTed or not on-disk. See [TOAST](braised:ref/storage-toast) for more information about TOAST.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_database_size` ( `name` ) bigint

   `pg_database_size` ( `oid` ) bigint

   Computes the total disk space used by the database with the specified name or OID. To use this function, you must have `CONNECT` privilege on the specified database (which is granted by default) or have privileges of the `pg_read_all_stats` role.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_indexes_size` ( `regclass` ) bigint

   Computes the total disk space used by indexes attached to the specified table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_relation_size` ( `relation` `regclass` \[, `fork` `text`\] ) bigint

   Computes the disk space used by one "fork" of the specified relation. (Note that for most purposes it is more convenient to use the higher-level functions `pg_total_relation_size` or `pg_table_size`, which sum the sizes of all forks.) With one argument, this returns the size of the main data fork of the relation. The second argument can be provided to specify which fork to examine:

   -   `main` returns the size of the main data fork of the relation.
   -   `fsm` returns the size of the Free Space Map (see [Free Space Map](braised:ref/storage-fsm)) associated with the relation.
   -   `vm` returns the size of the Visibility Map (see [Visibility Map](braised:ref/storage-vm)) associated with the relation.
   -   `init` returns the size of the initialization fork, if any, associated with the relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_size_bytes` ( `text` ) bigint

   Converts a size in human-readable format (as returned by `pg_size_pretty`) into bytes. Valid units are `bytes`, `B`, `kB`, `MB`, `GB`, `TB`, and `PB`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_size_pretty` ( `bigint` ) text

   `pg_size_pretty` ( `numeric` ) text

   Converts a size in bytes into a more easily human-readable format with size units (bytes, kB, MB, GB, TB, or PB as appropriate). Note that the units are powers of 2 rather than powers of 10, so 1kB is 1024 bytes, 1MB is 1024^2^ = 1048576 bytes, and so on.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_table_size` ( `regclass` ) bigint

   Computes the disk space used by the specified table, excluding indexes (but including its TOAST table if any, free space map, and visibility map).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_tablespace_size` ( `name` ) bigint

   `pg_tablespace_size` ( `oid` ) bigint

   Computes the total disk space used in the tablespace with the specified name or OID. To use this function, you must have `CREATE` privilege on the specified tablespace or have privileges of the `pg_read_all_stats` role, unless it is the default tablespace for the current database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_total_relation_size` ( `regclass` ) bigint

   Computes the total disk space used by the specified table, including all indexes and TOAST data. The result is equivalent to `pg_table_size` `+` `pg_indexes_size`.
  :::{/cell}
  :::{/row}
:::{/table}

: Database Object Size Functions

The functions above that operate on tables or indexes accept a `regclass` argument, which is simply the OID of the table or index in the pg_class system catalog. You do not have to look up the OID by hand, however, since the `regclass` data type\'s input converter will do the work for you. See [Object Identifier Types](braised:ref/datatype-oid) for details.

The functions shown in [Database Object Location Functions](#functions-admin-dblocation) assist in identifying the specific disk files associated with database objects.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_relation_filenode` ( `relation` `regclass` ) oid

   Returns the "filenode" number currently assigned to the specified relation. The filenode is the base component of the file name(s) used for the relation (see [Database File Layout](braised:ref/storage-file-layout) for more information). For most relations the result is the same as pg_class.relfilenode, but for certain system catalogs relfilenode is zero and this function must be used to get the correct value. The function returns NULL if passed a relation that does not have storage, such as a view.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_relation_filepath` ( `relation` `regclass` ) text

   Returns the entire file path name (relative to the database cluster\'s data directory, `PGDATA`) of the relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_filenode_relation` ( `tablespace` `oid`, `filenode` `oid` ) regclass

   Returns a relation\'s OID given the tablespace OID and filenode it is stored under. This is essentially the inverse mapping of `pg_relation_filepath`. For a relation in the database\'s default tablespace, the tablespace can be specified as zero. Returns `NULL` if no relation in the current database is associated with the given values, or if dealing with a temporary relation.
  :::{/cell}
  :::{/row}
:::{/table}

: Database Object Location Functions

[Collation Management Functions](#functions-admin-collation) lists functions used to manage collations.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_collation_actual_version` ( `oid` ) text

   Returns the actual version of the collation object as it is currently installed in the operating system. If this is different from the value in pg_collation.collversion, then objects depending on the collation might need to be rebuilt. See also [ALTER COLLATION](braised:ref/sql-altercollation).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_database_collation_actual_version` ( `oid` ) text

   Returns the actual version of the database\'s collation as it is currently installed in the operating system. If this is different from the value in pg_database.datcollversion, then objects depending on the collation might need to be rebuilt. See also [ALTER DATABASE](braised:ref/sql-alterdatabase).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_import_system_collations` ( `schema` `regnamespace` ) integer

   Adds collations to the system catalog pg_collation based on all the locales it finds in the operating system. This is what `initdb` uses; see [Managing Collations](braised:ref/collation#managing-collations) for more details. If additional locales are installed into the operating system later on, this function can be run again to add collations for the new locales. Locales that match existing entries in pg_collation will be skipped. (But collation objects based on locales that are no longer present in the operating system are not removed by this function.) The `schema` parameter would typically be `pg_catalog`, but that is not a requirement; the collations could be installed into some other schema as well. The function returns the number of new collation objects it created. Use of this function is restricted to superusers.
  :::{/cell}
  :::{/row}
:::{/table}

: Collation Management Functions

[Database Object Statistics Manipulation Functions](#functions-admin-statsmod) lists functions used to manipulate statistics. These functions cannot be executed during recovery.

:::{.callout type="warning"}
Changes made by these statistics manipulation functions are likely to be overwritten by [autovacuum](#autovacuum) (or manual `VACUUM` or `ANALYZE`) and should be considered temporary.
:::

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_restore_relation_stats` ( `VARIADIC` `kwargs` `"any"` ) boolean

   Updates table-level statistics. Ordinarily, these statistics are collected automatically or updated as a part of [VACUUM](braised:ref/sql-vacuum) or [ANALYZE](braised:ref/sql-analyze), so it\'s not necessary to call this function. However, it is useful after a restore to enable the optimizer to choose better plans if `ANALYZE` has not been run yet.

   The tracked statistics may change from version to version, so arguments are passed as pairs of *argname* and *argvalue* in the form:                                                                                                                                                                                                                                                                                                       |

       SELECT pg_restore_relation_stats(
           'arg1name', 'arg1value'::arg1type,
           'arg2name', 'arg2value'::arg2type,
           'arg3name', 'arg3value'::arg3type);

   For example, to set the relpages and reltuples values for the table mytable:

       SELECT pg_restore_relation_stats(
           'schemaname', 'myschema',
           'relname',    'mytable',
           'relpages',   173::integer,
           'reltuples',  10000::real);

   The arguments `schemaname` and `relname` are required, and specify the table. Other arguments are the names and values of statistics corresponding to certain columns in [pg_class](#catalog-pg-class). The currently-supported relation statistics are `relpages` with a value of type `integer`, `reltuples` with a value of type `real`, `relallvisible` with a value of type `integer`, and `relallfrozen` with a value of type `integer`.

   Additionally, this function accepts argument name `version` of type `integer`, which specifies the server version from which the statistics originated. This is anticipated to be helpful in porting statistics from older versions of PostgreSQL.

   Minor errors are reported as a `WARNING` and ignored, and remaining statistics will still be restored. If all specified statistics are successfully restored, returns `true`, otherwise `false`.

   The caller must have the `MAINTAIN` privilege on the table or be the owner of the database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_clear_relation_stats` ( `schemaname` `text`, `relname` `text` ) void

   Clears table-level statistics for the given relation, as though the table was newly created.

   The caller must have the `MAINTAIN` privilege on the table or be the owner of the database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_restore_attribute_stats` ( `VARIADIC` `kwargs` `"any"` ) boolean

   Creates or updates column-level statistics. Ordinarily, these statistics are collected automatically or updated as a part of [VACUUM](braised:ref/sql-vacuum) or [ANALYZE](braised:ref/sql-analyze), so it\'s not necessary to call this function. However, it is useful after a restore to enable the optimizer to choose better plans if `ANALYZE` has not been run yet.

   The tracked statistics may change from version to version, so arguments are passed as pairs of *argname* and *argvalue* in the form:                                                                                                                                                                                                                                                                                                       |

       SELECT pg_restore_attribute_stats(
           'arg1name', 'arg1value'::arg1type,
           'arg2name', 'arg2value'::arg2type,
           'arg3name', 'arg3value'::arg3type);

   For example, to set the avg_width and null_frac values for the attribute col1 of the table mytable:

       SELECT pg_restore_attribute_stats(
           'schemaname', 'myschema',
           'relname',    'mytable',
           'attname',    'col1',
           'inherited',  false,
           'avg_width',  125::integer,
           'null_frac',  0.5::real);

   The required arguments are `schemaname` and `relname` with a value of type `text` which specify the table; either `attname` with a value of type `text` or `attnum` with a value of type `smallint`, which specifies the column; and `inherited`, which specifies whether the statistics include values from child tables. Other arguments are the names and values of statistics corresponding to columns in [pg_stats](#view-pg-stats).

   Additionally, this function accepts argument name `version` of type `integer`, which specifies the server version from which the statistics originated. This is anticipated to be helpful in porting statistics from older versions of PostgreSQL.

   Minor errors are reported as a `WARNING` and ignored, and remaining statistics will still be restored. If all specified statistics are successfully restored, returns `true`, otherwise `false`.

   The caller must have the `MAINTAIN` privilege on the table or be the owner of the database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_clear_attribute_stats` ( `schemaname` `text`, `relname` `text`, `attname` `text`, `inherited` `boolean` ) void

   Clears column-level statistics for the given relation and attribute, as though the table was newly created.

   The caller must have the `MAINTAIN` privilege on the table or be the owner of the database.
  :::{/cell}
  :::{/row}
:::{/table}

: Database Object Statistics Manipulation Functions

[Partitioning Information Functions](#functions-info-partition) lists functions that provide information about the structure of partitioned tables.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_partition_tree` ( `regclass` ) setof record ( `relid` `regclass`, `parentrelid` `regclass`, `isleaf` `boolean`, `level` `integer` )

   Lists the tables or indexes in the partition tree of the given partitioned table or partitioned index, with one row for each partition. Information provided includes the OID of the partition, the OID of its immediate parent, a boolean value telling if the partition is a leaf, and an integer telling its level in the hierarchy. The level value is 0 for the input table or index, 1 for its immediate child partitions, 2 for their partitions, and so on. Returns no rows if the relation does not exist or is not a partition or partitioned table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_partition_ancestors` ( `regclass` ) setof regclass

   Lists the ancestor relations of the given partition, including the relation itself. Returns no rows if the relation does not exist or is not a partition or partitioned table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_partition_root` ( `regclass` ) regclass

   Returns the top-most parent of the partition tree to which the given relation belongs. Returns `NULL` if the relation does not exist or is not a partition or partitioned table.
  :::{/cell}
  :::{/row}
:::{/table}

: Partitioning Information Functions

For example, to check the total size of the data contained in a partitioned table measurement, one could use the following query:

    SELECT pg_size_pretty(sum(pg_relation_size(relid))) AS total_size
      FROM pg_partition_tree('measurement');

### Index Maintenance Functions

Index Maintenance Functions shows the functions available for index maintenance tasks. (Note that these maintenance tasks are normally done automatically by autovacuum; use of these functions is only required in special cases.) These functions cannot be executed during recovery. Use of these functions is restricted to superusers and the owner of the given index.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `brin_summarize_new_values` ( `index` `regclass` ) integer

   Scans the specified BRIN index to find page ranges in the base table that are not currently summarized by the index; for any such range it creates a new summary index tuple by scanning those table pages. Returns the number of new page range summaries that were inserted into the index.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `brin_summarize_range` ( `index` `regclass`, `blockNumber` `bigint` ) integer

   Summarizes the page range covering the given block, if not already summarized. This is like `brin_summarize_new_values` except that it only processes the page range that covers the given table block number.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `brin_desummarize_range` ( `index` `regclass`, `blockNumber` `bigint` ) void

   Removes the BRIN index tuple that summarizes the page range covering the given table block, if there is one.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `gin_clean_pending_list` ( `index` `regclass` ) bigint

   Cleans up the "pending" list of the specified GIN index by moving entries in it, in bulk, to the main GIN data structure. Returns the number of pages removed from the pending list. If the argument is a GIN index built with the `fastupdate` option disabled, no cleanup happens and the result is zero, because the index doesn\'t have a pending list. See [GIN Fast Update Technique](braised:ref/gin#gin-fast-update-technique) and [GIN Tips and Tricks](braised:ref/gin#gin-tips-and-tricks) for details about the pending list and `fastupdate` option.
  :::{/cell}
  :::{/row}
:::{/table}

: Index Maintenance Functions

### Generic File Access Functions

The functions shown in Generic File Access Functions provide native access to files on the machine hosting the server. Only files within the database cluster directory and the `log_directory` can be accessed, unless the user is a superuser or is granted the role `pg_read_server_files`. Use a relative path for files in the cluster directory, and a path matching the `log_directory` configuration setting for log files.

Note that granting users the EXECUTE privilege on `pg_read_file()`, or related functions, allows them the ability to read any file on the server that the database server process can read; these functions bypass all in-database privilege checks. This means that, for example, a user with such access is able to read the contents of the pg_authid table where authentication information is stored, as well as read any table data in the database. Therefore, granting access to these functions should be carefully considered.

When granting privilege on these functions, note that the table entries showing optional parameters are mostly implemented as several physical functions with different parameter lists. Privilege must be granted separately on each such function, if it is to be used. psql\'s `\df` command can be useful to check what the actual function signatures are.

Some of these functions take an optional `missing_ok` parameter, which specifies the behavior when the file or directory does not exist. If `true`, the function returns `NULL` or an empty result set, as appropriate. If `false`, an error is raised. (Failure conditions other than "file not found" are reported as errors in any case.) The default is `false`.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_dir` ( `dirname` `text` \[, `missing_ok` `boolean`, `include_dot_dirs` `boolean`\] ) setof text

   Returns the names of all files (and directories and other special files) in the specified directory. The `include_dot_dirs` parameter indicates whether "." and ".." are to be included in the result set; the default is to exclude them. Including them can be useful when `missing_ok` is `true`, to distinguish an empty directory from a non-existent directory.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_logdir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s log directory. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and roles with privileges of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_waldir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s write-ahead log (WAL) directory. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and roles with privileges of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_logicalmapdir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s `pg_logical/mappings` directory. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_logicalsnapdir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s `pg_logical/snapshots` directory. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_replslotdir` ( `slot_name` `text` ) setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s `pg_replslot/slot_name` directory, where `slot_name` is the name of the replication slot provided as input of the function. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_summariesdir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s WAL summaries directory (`pg_wal/summaries`). Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_archive_statusdir` () setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the server\'s WAL archive status directory (`pg_wal/archive_status`). Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_ls_tmpdir` ( \[`tablespace` `oid`\] ) setof record ( `name` `text`, `size` `bigint`, `modification` `timestamp with time zone` )

   Returns the name, size, and last modification time (mtime) of each ordinary file in the temporary file directory for the specified `tablespace`. If `tablespace` is not provided, the `pg_default` tablespace is examined. Filenames beginning with a dot, directories, and other special files are excluded.

   This function is restricted to superusers and members of the `pg_monitor` role by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_read_file` ( `filename` `text` \[, `offset` `bigint`, `length` `bigint`\] \[, `missing_ok` `boolean`\] ) text

   Returns all or part of a text file, starting at the given byte `offset`, returning at most `length` bytes (less if the end of file is reached first). If `offset` is negative, it is relative to the end of the file. If `offset` and `length` are omitted, the entire file is returned. The bytes read from the file are interpreted as a string in the database\'s encoding; an error is thrown if they are not valid in that encoding.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_read_binary_file` ( `filename` `text` \[, `offset` `bigint`, `length` `bigint`\] \[, `missing_ok` `boolean`\] ) bytea

   Returns all or part of a file. This function is identical to `pg_read_file` except that it can read arbitrary binary data, returning the result as `bytea` not `text`; accordingly, no encoding checks are performed.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.

   In combination with the `convert_from` function, this function can be used to read a text file in a specified encoding and convert to the database\'s encoding:

       SELECT convert_from(pg_read_binary_file('file_in_utf8.txt'), 'UTF8');
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_stat_file` ( `filename` `text` \[, `missing_ok` `boolean`\] ) record ( `size` `bigint`, `access` `timestamp with time zone`, `modification` `timestamp with time zone`, `change` `timestamp with time zone`, `creation` `timestamp with time zone`, `isdir` `boolean` )

   Returns a record containing the file\'s size, last access time stamp, last modification time stamp, last file status change time stamp (Unix platforms only), file creation time stamp (Windows only), and a flag indicating if it is a directory.

   This function is restricted to superusers by default, but other users can be granted EXECUTE to run the function.
  :::{/cell}
  :::{/row}
:::{/table}

: Generic File Access Functions

### Advisory Lock Functions

The functions shown in Advisory Lock Functions manage advisory locks. For details about proper use of these functions, see [Advisory Locks](braised:ref/explicit-locking#advisory-locks).

All these functions are intended to be used to lock application-defined resources, which can be identified either by a single 64-bit key value or two 32-bit key values (note that these two key spaces do not overlap). If another session already holds a conflicting lock on the same resource identifier, the functions will either wait until the resource becomes available, or return a `false` result, as appropriate for the function. Locks can be either shared or exclusive: a shared lock does not conflict with other shared locks on the same resource, only with exclusive locks. Locks can be taken at session level (so that they are held until released or the session ends) or at transaction level (so that they are held until the current transaction ends; there is no provision for manual release). Multiple session-level lock requests stack, so that if the same resource identifier is locked three times there must then be three unlock requests to release the resource in advance of session end.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_lock` ( `key` `bigint` ) void

   `pg_advisory_lock` ( `key1` `integer`, `key2` `integer` ) void

   Obtains an exclusive session-level advisory lock, waiting if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_lock_shared` ( `key` `bigint` ) void

   `pg_advisory_lock_shared` ( `key1` `integer`, `key2` `integer` ) void

   Obtains a shared session-level advisory lock, waiting if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_unlock` ( `key` `bigint` ) boolean

   `pg_advisory_unlock` ( `key1` `integer`, `key2` `integer` ) boolean

   Releases a previously-acquired exclusive session-level advisory lock. Returns `true` if the lock is successfully released. If the lock was not held, `false` is returned, and in addition, an SQL warning will be reported by the server.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_unlock_all` () void

   Releases all session-level advisory locks held by the current session. (This function is implicitly invoked at session end, even if the client disconnects ungracefully.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_unlock_shared` ( `key` `bigint` ) boolean

   `pg_advisory_unlock_shared` ( `key1` `integer`, `key2` `integer` ) boolean

   Releases a previously-acquired shared session-level advisory lock. Returns `true` if the lock is successfully released. If the lock was not held, `false` is returned, and in addition, an SQL warning will be reported by the server.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_xact_lock` ( `key` `bigint` ) void

   `pg_advisory_xact_lock` ( `key1` `integer`, `key2` `integer` ) void

   Obtains an exclusive transaction-level advisory lock, waiting if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_advisory_xact_lock_shared` ( `key` `bigint` ) void

   `pg_advisory_xact_lock_shared` ( `key1` `integer`, `key2` `integer` ) void

   Obtains a shared transaction-level advisory lock, waiting if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_try_advisory_lock` ( `key` `bigint` ) boolean

   `pg_try_advisory_lock` ( `key1` `integer`, `key2` `integer` ) boolean

   Obtains an exclusive session-level advisory lock if available. This will either obtain the lock immediately and return `true`, or return `false` without waiting if the lock cannot be acquired immediately.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_try_advisory_lock_shared` ( `key` `bigint` ) boolean

   `pg_try_advisory_lock_shared` ( `key1` `integer`, `key2` `integer` ) boolean

   Obtains a shared session-level advisory lock if available. This will either obtain the lock immediately and return `true`, or return `false` without waiting if the lock cannot be acquired immediately.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_try_advisory_xact_lock` ( `key` `bigint` ) boolean

   `pg_try_advisory_xact_lock` ( `key1` `integer`, `key2` `integer` ) boolean

   Obtains an exclusive transaction-level advisory lock if available. This will either obtain the lock immediately and return `true`, or return `false` without waiting if the lock cannot be acquired immediately.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_try_advisory_xact_lock_shared` ( `key` `bigint` ) boolean

   `pg_try_advisory_xact_lock_shared` ( `key1` `integer`, `key2` `integer` ) boolean

   Obtains a shared transaction-level advisory lock if available. This will either obtain the lock immediately and return `true`, or return `false` without waiting if the lock cannot be acquired immediately.
  :::{/cell}
  :::{/row}
:::{/table}

: Advisory Lock Functions
