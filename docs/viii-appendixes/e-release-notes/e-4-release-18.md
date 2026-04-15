---
title: "E.4. Release 18"
id: release-18
---

**Release date:**

2025-09-25

### Overview

PostgreSQL 18 contains many new features and enhancements, including:

-   An asynchronous I/O (AIO) subsystem that can improve performance of sequential scans, bitmap heap scans, vacuums, and other operations.

-   [pg_upgrade](#pgupgrade) now retains optimizer statistics.

-   Support for \"skip scan\" lookups that allow using [multicolumn B-tree indexes](#indexes-multicolumn) in more cases.

-   [`uuidv7()`](#func_uuid_gen_table) function for generating timestamp-ordered [UUIDs](#datatype-uuid).

-   Virtual [generated columns](#sql-createtable-parms-generated-stored) that compute their values during read operations. This is now the default for generated columns.

-   [OAuth authentication](#auth-oauth) support.

-   `OLD` and `NEW` support for [`RETURNING`](#dml-returning) clauses in [INSERT](braised:ref/sql-insert), [UPDATE](braised:ref/sql-update), [DELETE](braised:ref/sql-delete), and [MERGE](braised:ref/sql-merge) commands.

-   Temporal constraints, or constraints over ranges, for [PRIMARY KEY](#sql-createtable-parms-primary-key), [UNIQUE](#sql-createtable-parms-unique), and [FOREIGN KEY](#sql-createtable-parms-references) constraints.

The above items and other new features of PostgreSQL 18 are explained in more detail in the sections below.

### Migration to Version 18

A dump/restore using [pg_dumpall](braised:ref/app-pg-dumpall) or use of [pg_upgrade](braised:ref/pgupgrade) or logical replication is required for those wishing to migrate data from any previous release.
See [Upgrading a PostgreSQL Cluster](braised:ref/upgrading) for general information on migrating to new major releases.

Version 18 contains a number of changes that may affect compatibility with previous releases.
Observe the following incompatibilities:

-   Change [initdb](braised:ref/app-initdb) default to enable data checksums (Greg Sabino Mullane) [](https://postgr.es/c/04bec894a04)

    Checksums can be disabled with the new initdb option `--no-data-checksums`. [pg_upgrade](braised:ref/pgupgrade) requires matching cluster checksum settings, so this new option can be useful to upgrade non-checksum old clusters.

-   Change time zone abbreviation handling (Tom Lane) [](https://postgr.es/c/d7674c9fa)

    The system will now favor the current session\'s time zone abbreviations before checking the server variable [timezone_abbreviations (string)
      
       timezone_abbreviations configuration parameter
      
      time zone names](braised:ref/runtime-config-client#timezone-abbreviations-string-timezone-abbreviations-configuration-parameter-time-zone-names). Previously `timezone_abbreviations` was checked first.

-   Deprecate [MD5 password](#auth-password) authentication (Nathan Bossart) [](https://postgr.es/c/db6a4a985)

    Support for MD5 passwords will be removed in a future major version release. [CREATE ROLE](braised:ref/sql-createrole) and [ALTER ROLE](braised:ref/sql-alterrole) now emit deprecation warnings when setting MD5 passwords. These warnings can be disabled by setting the [md5_password_warnings (boolean)
      
       md5_password_warnings configuration parameter](braised:ref/runtime-config-connection#md5-password-warnings-boolean-md5-password-warnings-configuration-parameter) parameter to `off`.

-   Change [VACUUM](braised:ref/sql-vacuum) and [ANALYZE](braised:ref/sql-analyze) to process the inheritance children of a parent (Michael Harris) [](https://postgr.es/c/62ddf7ee9)

    The previous behavior can be performed by using the new `ONLY` option.

-   Prevent [`COPY FROM`](#sql-copy) from treating `\.` as an end-of-file marker when reading CSV files (Daniel Vérité, Tom Lane) [](https://postgr.es/c/770233748) [](https://postgr.es/c/da8a4c166)

    [psql](braised:ref/app-psql) will still treat `\.` as an end-of-file marker when reading CSV files from `STDIN`. Older psql clients connecting to PostgreSQL 18 servers might experience [`\copy`](#app-psql-meta-commands-copy) problems. This release also enforces that `\.` must appear alone on a line.

-   Disallow unlogged partitioned tables (Michael Paquier) [](https://postgr.es/c/e2bab2d79)

    Previously [`ALTER TABLE SET [UN]LOGGED`](#sql-altertable) did nothing, and the creation of an unlogged partitioned table did not cause its children to be unlogged.

-   Execute `AFTER` [triggers](#triggers) as the role that was active when trigger events were queued (Laurenz Albe) [](https://postgr.es/c/01463e1cc)

    Previously such triggers were run as the role that was active at trigger execution time (e.g., at [COMMIT](braised:ref/sql-commit)). This is significant for cases where the role is changed between queue time and transaction commit.

-   Remove non-functional support for rule privileges in [GRANT](braised:ref/sql-grant)/[REVOKE](braised:ref/sql-revoke) (Fujii Masao) [](https://postgr.es/c/fefa76f70)

    These have been non-functional since PostgreSQL 8.2.

-   Remove column [pg_backend_memory_contexts](#view-pg-backend-memory-contexts).parent (Melih Mutlu) [](https://postgr.es/c/f0d112759)

    This is no longer needed since pg_backend_memory_contexts.path was added.

-   Change pg_backend_memory_contexts.level and `pg_log_backend_memory_contexts()` to be one-based (Melih Mutlu, Atsushi Torikoshi, David Rowley, Fujii Masao) [](https://postgr.es/c/32d3ed816) [](https://postgr.es/c/d9e03864b) [](https://postgr.es/c/706cbed35)

    These were previously zero-based.

-   Change [full text search](#textsearch) to use the default collation provider of the cluster to read configuration files and dictionaries, rather than always using libc (Peter Eisentraut) [](https://postgr.es/c/fb1a18810f0)

    Clusters that default to non-libc collation providers (e.g., ICU, builtin) that behave differently than libc for characters processed by LC_CTYPE could observe changes in behavior of some full-text search functions, as well as the [F.35. pg_trgm — support for similarity of text using trigram matching](braised:ref/pgtrgm) extension. When upgrading such clusters using [pg_upgrade](braised:ref/pgupgrade), it is recommended to reindex all indexes related to full-text search and pg_trgm after the upgrade.

### Changes

Below you will find a detailed account of the changes between PostgreSQL 18 and the previous major release.

#### Server

##### Optimizer

-   Automatically remove some unnecessary table self-joins (Andrey Lepikhov, Alexander Kuzmenkov, Alexander Korotkov, Alena Rybakina) [](https://postgr.es/c/fc069a3a6)

    This optimization can be disabled using server variable [enable_self_join_elimination (boolean)
      
       enable_self_join_elimination configuration parameter](braised:ref/runtime-config-query#enable-self-join-elimination-boolean-enable-self-join-elimination-configuration-parameter).

-   Convert some [`IN (VALUES ...)`](#functions-comparisons-in-scalar) to `x = ANY ...` for better optimizer statistics (Alena Rybakina, Andrei Lepikhov) [](https://postgr.es/c/c0962a113)

-   Allow transforming [`OR`](#functions-logical)-clauses to arrays for faster index processing (Alexander Korotkov, Andrey Lepikhov) [](https://postgr.es/c/ae4569161)

-   Speed up the processing of [`INTERSECT`](#sql-intersect), [`EXCEPT`](#sql-except), [window aggregates](#tutorial-window), and [view column aliases](#sql-createview) (Tom Lane, David Rowley) [](https://postgr.es/c/52c707483) [](https://postgr.es/c/276279295) [](https://postgr.es/c/8d96f57d5) [](https://postgr.es/c/908a96861)

-   Allow the keys of [`SELECT DISTINCT`](#sql-distinct) to be internally reordered to avoid sorting (Richard Guo) [](https://postgr.es/c/a8ccf4e93)

    This optimization can be disabled using [enable_distinct_reordering (boolean)
      
       enable_distinct_reordering configuration parameter](braised:ref/runtime-config-query#enable-distinct-reordering-boolean-enable-distinct-reordering-configuration-parameter).

-   Ignore [`GROUP BY`](#sql-groupby) columns that are functionally dependent on other columns (Zhang Mingli, Jian He, David Rowley) [](https://postgr.es/c/bd10ec529)

    If a `GROUP BY` clause includes all columns of a unique index, as well as other columns of the same table, those other columns are redundant and can be dropped from the grouping. This was already true for non-deferred primary keys.

-   Allow some [`HAVING`](#sql-having) clauses on [`GROUPING SETS`](#queries-grouping-sets) to be pushed to [`WHERE`](#sql-where) clauses (Richard Guo) [](https://postgr.es/c/67a54b9e8) [](https://postgr.es/c/247dea89f) [](https://postgr.es/c/f5050f795) [](https://postgr.es/c/cc5d98525)

    This allows earlier row filtering. This release also fixes some `GROUPING SETS` queries that used to return incorrect results.

-   Improve row estimates for [`generate_series()`](#functions-srf-series) using [`numeric`](#datatype-numeric) and [`timestamp`](#datatype-datetime) values (David Rowley, Song Jinzhou) [](https://postgr.es/c/036bdcec9) [](https://postgr.es/c/97173536e)

-   Allow the optimizer to use `Right Semi Join` plans (Richard Guo) [](https://postgr.es/c/aa86129e1)

    Semi-joins are used when needing to find if there is at least one match.

-   Allow merge joins to use incremental sorts (Richard Guo) [](https://postgr.es/c/828e94c9d)

-   Improve the efficiency of planning queries accessing many partitions (Ashutosh Bapat, Yuya Watari, David Rowley) [](https://postgr.es/c/88f55bc97) [](https://postgr.es/c/d69d45a5a)

-   Allow partitionwise joins in more cases, and reduce its memory usage (Richard Guo, Tom Lane, Ashutosh Bapat) [](https://postgr.es/c/9b282a935) [](https://postgr.es/c/513f4472a)

-   Improve cost estimates of partition queries (Nikita Malakhov, Andrei Lepikhov) [](https://postgr.es/c/fae535da0)

-   Improve [SQL-language function](#xfunc-sql) plan caching (Alexander Pyhalov, Tom Lane) [](https://postgr.es/c/0dca5d68d) [](https://postgr.es/c/09b07c295)

-   Improve handling of disabled optimizer features (Robert Haas) [](https://postgr.es/c/e22253467)

##### Indexes

-   Allow skip scans of [btree](#xfunc-sql) indexes (Peter Geoghegan) [](https://postgr.es/c/92fe23d93) [](https://postgr.es/c/8a510275d)

    This allows multi-column btree indexes to be used in more cases such as when there are no restrictions on the first or early indexed columns (or there are non-equality ones), and there are useful restrictions on later indexed columns.

-   Allow non-btree unique indexes to be used as partition keys and in materialized views (Mark Dilger) [](https://postgr.es/c/f278e1fe3) [](https://postgr.es/c/9d6db8bec)

    The index type must still support equality.

-   Allow [`GIN`](#gin) indexes to be created in parallel (Tomas Vondra, Matthias van de Meent) [](https://postgr.es/c/8492feb98)

-   Allow values to be sorted to speed range-type [GiST](#gist) and [btree](#btree) index builds (Bernd Helmle) [](https://postgr.es/c/e9e7b6604)

##### General Performance

-   Add an asynchronous I/O subsystem (Andres Freund, Thomas Munro, Nazir Bilal Yavuz, Melanie Plageman) [](https://postgr.es/c/02844012b) [](https://postgr.es/c/da7226993) [](https://postgr.es/c/55b454d0e) [](https://postgr.es/c/247ce06b8) [](https://postgr.es/c/10f664684) [](https://postgr.es/c/06fb5612c) [](https://postgr.es/c/c325a7633) [](https://postgr.es/c/50cb7505b) [](https://postgr.es/c/047cba7fa) [](https://postgr.es/c/12ce89fd0) [](https://postgr.es/c/2a5e709e7)

    This feature allows backends to queue multiple read requests, which allows for more efficient sequential scans, bitmap heap scans, vacuums, etc. This is enabled by server variable [io_method (enum)
       
        io_method configuration parameter](braised:ref/runtime-config-resource#io-method-enum-io-method-configuration-parameter), with server variables [io_combine_limit (integer)
       
        io_combine_limit configuration parameter](braised:ref/runtime-config-resource#io-combine-limit-integer-io-combine-limit-configuration-parameter) and [io_max_combine_limit (integer)
       
        io_max_combine_limit configuration parameter](braised:ref/runtime-config-resource#io-max-combine-limit-integer-io-max-combine-limit-configuration-parameter) added to control it. This also enables [effective_io_concurrency (integer)
       
        effective_io_concurrency configuration parameter](braised:ref/runtime-config-resource#effective-io-concurrency-integer-effective-io-concurrency-configuration-parameter) and [maintenance_io_concurrency (integer)
       
        maintenance_io_concurrency configuration parameter](braised:ref/runtime-config-resource#maintenance-io-concurrency-integer-maintenance-io-concurrency-configuration-parameter) values greater than zero for systems without `fadvise()` support. The new system view [pg_aios](#view-pg-aios) shows the file handles being used for asynchronous I/O.

-   Improve the locking performance of queries that access many relations (Tomas Vondra) [](https://postgr.es/c/c4d5cb71d)

-   Improve the performance and reduce memory usage of hash joins and [`GROUP BY`](#sql-groupby) (David Rowley, Jeff Davis) [](https://postgr.es/c/adf97c156) [](https://postgr.es/c/0f5738202) [](https://postgr.es/c/4d143509c) [](https://postgr.es/c/a0942f441) [](https://postgr.es/c/626df47ad)

    This also improves hash set operations used by [`EXCEPT`](#sql-except), and hash lookups of subplan values.

-   Allow normal vacuums to freeze some pages, even though they are all-visible (Melanie Plageman) [](https://postgr.es/c/052026c9b) [](https://postgr.es/c/06eae9e62)

    This reduces the overhead of later full-relation freezing. The aggressiveness of this can be controlled by server variable and per-table setting [vacuum_max_eager_freeze_failure_rate (floating point)
      
       vacuum_max_eager_freeze_failure_rate
       configuration parameter](braised:ref/runtime-config-vacuum#vacuum-max-eager-freeze-failure-rate-floating-point-vacuum-max-eager-freeze-failure-rate-configuration-parameter). Previously vacuum never processed all-visible pages until freezing was required.

-   Add server variable [vacuum_truncate (boolean)
       
        vacuum_truncate
        configuration parameter](braised:ref/runtime-config-vacuum#vacuum-truncate-boolean-vacuum-truncate-configuration-parameter) to control file truncation during [VACUUM](braised:ref/sql-vacuum) (Nathan Bossart, Gurjeet Singh) [](https://postgr.es/c/0164a0f9e)

    A storage-level parameter with the same name and behavior already existed.

-   Increase server variables [effective_io_concurrency (integer)
       
        effective_io_concurrency configuration parameter](braised:ref/runtime-config-resource#effective-io-concurrency-integer-effective-io-concurrency-configuration-parameter)\'s and [maintenance_io_concurrency (integer)
       
        maintenance_io_concurrency configuration parameter](braised:ref/runtime-config-resource#maintenance-io-concurrency-integer-maintenance-io-concurrency-configuration-parameter)\'s default values to 16 (Melanie Plageman) [](https://postgr.es/c/ff79b5b2a) [](https://postgr.es/c/cc6be07eb)

    This more accurately reflects modern hardware.

##### Monitoring

-   Increase the logging granularity of server variable [log_connections (string)
      
       log_connections configuration parameter](braised:ref/runtime-config-logging#log-connections-string-log-connections-configuration-parameter) (Melanie Plageman) [](https://postgr.es/c/9219093ca)

    This server variable was previously only boolean, which is still supported.

-   Add `log_connections` option to report the duration of connection stages (Melanie Plageman) [](https://postgr.es/c/18cd15e70)

-   Add [log_line_prefix (string)
      
       log_line_prefix configuration parameter](braised:ref/runtime-config-logging#log-line-prefix-string-log-line-prefix-configuration-parameter) escape `%L` to output the client IP address (Greg Sabino Mullane) [](https://postgr.es/c/3516ea768)

-   Add server variable [log_lock_failures (boolean)
      
       log_lock_failures configuration parameter](braised:ref/runtime-config-logging#log-lock-failures-boolean-log-lock-failures-configuration-parameter) to log lock acquisition failures (Yuki Seino, Fujii Masao) [](https://postgr.es/c/6d376c3b0) [](https://postgr.es/c/73bdcfab3)

    Specifically it reports [`SELECT ... NOWAIT`](#sql-for-update-share) lock failures.

-   Modify [pg_stat_all_tables](#monitoring-pg-stat-all-tables-view) and its variants to report the time spent in [VACUUM](braised:ref/sql-vacuum), [ANALYZE](braised:ref/sql-analyze), and their [automatic](#autovacuum) variants (Sami Imseih) [](https://postgr.es/c/30a6ed0ce)

    The new columns are total_vacuum_time, total_autovacuum_time, total_analyze_time, and total_autoanalyze_time.

-   Add delay time reporting to [VACUUM](braised:ref/sql-vacuum) and [ANALYZE](braised:ref/sql-analyze) (Bertrand Drouvot, Nathan Bossart) [](https://postgr.es/c/bb8dff999) [](https://postgr.es/c/7720082ae)

    This information appears in the server log, the system views [pg_stat_progress_vacuum](#vacuum-progress-reporting) and [pg_stat_progress_analyze](#pg-stat-progress-analyze-view), and the output of [VACUUM](braised:ref/sql-vacuum) and [ANALYZE](braised:ref/sql-analyze) when in `VERBOSE` mode; tracking must be enabled with the server variable [track_cost_delay_timing (boolean)
      
       track_cost_delay_timing configuration parameter](braised:ref/runtime-config-statistics#track-cost-delay-timing-boolean-track-cost-delay-timing-configuration-parameter).

-   Add WAL, CPU, and average read statistics output to `ANALYZE VERBOSE` (Anthonin Bonnefoy) [](https://postgr.es/c/4c1b4cdb8) [](https://postgr.es/c/bb7775234)

-   Add full WAL buffer count to `VACUUM`/`ANALYZE (VERBOSE)` and autovacuum log output (Bertrand Drouvot) [](https://postgr.es/c/6a8a7ce47)

-   Add per-backend I/O statistics reporting (Bertrand Drouvot) [](https://postgr.es/c/9aea73fc6) [](https://postgr.es/c/3f1db99bf)

    The statistics are accessed via [`pg_stat_get_backend_io()`](#pg-stat-get-backend-io). Per-backend I/O statistics can be cleared via `pg_stat_reset_backend_stats()`.

-   Add [pg_stat_io](#monitoring-pg-stat-io-view) columns to report I/O activity in bytes (Nazir Bilal Yavuz) [](https://postgr.es/c/f92c854cf)

    The new columns are read_bytes, write_bytes, and extend_bytes. The op_bytes column, which always equaled `BLCKSZ`, has been removed.

-   Add WAL I/O activity rows to pg_stat_io (Nazir Bilal Yavuz, Bertrand Drouvot, Michael Paquier) [](https://postgr.es/c/a051e71e2) [](https://postgr.es/c/4538bd3f1) [](https://postgr.es/c/7f7f324eb)

    This includes WAL receiver activity and a wait event for such writes.

-   Change server variable [track_wal_io_timing (boolean)
      
       track_wal_io_timing configuration parameter](braised:ref/runtime-config-statistics#track-wal-io-timing-boolean-track-wal-io-timing-configuration-parameter) to control tracking WAL timing in pg_stat_io instead of [pg_stat_wal](#pg-stat-wal-view) (Bertrand Drouvot) [](https://postgr.es/c/6c349d83b)

-   Remove read/sync columns from pg_stat_wal (Bertrand Drouvot) [](https://postgr.es/c/2421e9a51) [](https://postgr.es/c/6c349d83b)

    This removes columns wal_write, wal_sync, wal_write_time, and wal_sync_time.

-   Add function [`pg_stat_get_backend_wal()`](#pg-stat-get-backend-wal) to return per-backend WAL statistics (Bertrand Drouvot) [](https://postgr.es/c/76def4cdd)

    Per-backend WAL statistics can be cleared via `pg_stat_reset_backend_stats()`.

-   Add function `pg_ls_summariesdir()` to specifically list the contents of [`PGDATA`](#storage-file-layout)/`pg_wal/summaries` (Yushi Ogiwara) [](https://postgr.es/c/4e1fad378)

-   Add column [pg_stat_checkpointer](#monitoring-pg-stat-checkpointer-view).num_done to report the number of completed checkpoints (Anton A. Melnikov) [](https://postgr.es/c/559efce1d)

    Columns num_timed and num_requested count both completed and skipped checkpoints.

-   Add column pg_stat_checkpointer.slru_written to report SLRU buffers written (Nitin Jadhav) [](https://postgr.es/c/17cc5f666)

    Also, modify the checkpoint server log message to report separate shared buffer and SLRU buffer values.

-   Add columns to [pg_stat_database](#monitoring-pg-stat-database-view) to report parallel worker activity (Benoit Lobréau) [](https://postgr.es/c/e7a9496de)

    The new columns are parallel_workers_to_launch and parallel_workers_launched.

-   Have query id computation of constant lists consider only the first and last constants (Dmitry Dolgov, Sami Imseih) [](https://postgr.es/c/62d712ecf) [](https://postgr.es/c/9fbd53dea) [](https://postgr.es/c/c2da1a5d6)

    Jumbling is used by [F.32. pg_stat_statements — track statistics of SQL planning and execution](braised:ref/pgstatstatements).

-   Adjust query id computations to group together queries using the same relation name (Michael Paquier, Sami Imseih) [](https://postgr.es/c/787514b30)

    This is true even if the tables in different schemas have different column names.

-   Add column [pg_backend_memory_contexts](#view-pg-backend-memory-contexts).type to report the type of memory context (David Rowley) [](https://postgr.es/c/12227a1d5)

-   Add column pg_backend_memory_contexts.path to show memory context parents (Melih Mutlu) [](https://postgr.es/c/32d3ed816)

##### Privileges

-   Add function `pg_get_acl()` to retrieve database access control details (Joel Jacobson) [](https://postgr.es/c/4564f1ceb) [](https://postgr.es/c/d898665bf)

-   Add function `has_largeobject_privilege()` to check large object privileges (Yugo Nagata) [](https://postgr.es/c/4eada203a)

-   Allow [ALTER DEFAULT PRIVILEGES](braised:ref/sql-alterdefaultprivileges) to define large object default privileges (Takatsuka Haruka, Yugo Nagata, Laurenz Albe) [](https://postgr.es/c/0d6c47766)

-   Add predefined role [`pg_signal_autovacuum_worker`](#predefined-roles) (Kirill Reshke) [](https://postgr.es/c/ccd38024b)

    This allows sending signals to autovacuum workers.

##### Server Configuration

-   Add support for the [OAuth authentication method](#auth-oauth) (Jacob Champion, Daniel Gustafsson, Thomas Munro) [](https://postgr.es/c/b3f0be788)

    This adds an `oauth` authentication method to [`pg_hba.conf`](#auth-pg-hba-conf), libpq OAuth options, a server variable [oauth_validator_libraries (string)
      
       oauth_validator_libraries configuration parameter](braised:ref/runtime-config-connection#oauth-validator-libraries-string-oauth-validator-libraries-configuration-parameter) to load token validation libraries, and a configure flag [`--with-libcurl`](#configure-option-with-libcurl) to add the required compile-time libraries.

-   Add server variable [ssl_tls13_ciphers (string)
      
       ssl_tls13_ciphers configuration parameter](braised:ref/runtime-config-connection#ssl-tls13-ciphers-string-ssl-tls13-ciphers-configuration-parameter) to allow specification of multiple colon-separated TLSv1.3 cipher suites (Erica Zhang, Daniel Gustafsson) [](https://postgr.es/c/45188c2ea)

-   Change server variable [ssl_groups (string)
      
       ssl_groups configuration parameter](braised:ref/runtime-config-connection#ssl-groups-string-ssl-groups-configuration-parameter)\'s default to include elliptic curve X25519 (Daniel Gustafsson, Jacob Champion) [](https://postgr.es/c/daa02c6bd)

-   Rename server variable `ssl_ecdh_curve` to [ssl_groups (string)
      
       ssl_groups configuration parameter](braised:ref/runtime-config-connection#ssl-groups-string-ssl-groups-configuration-parameter) and allow multiple colon-separated ECDH curves to be specified (Erica Zhang, Daniel Gustafsson) [](https://postgr.es/c/3d1ef3a15)

    The previous name still works.

-   Make cancel request keys 256 bits (Heikki Linnakangas, Jelte Fennema-Nio) [](https://postgr.es/c/a460251f0) [](https://postgr.es/c/9d9b9d46f)

    This is only possible when the server and client support wire protocol version 3.2, introduced in this release.

-   Add server variable [autovacuum_worker_slots (integer)
       
        autovacuum_worker_slots configuration parameter](braised:ref/runtime-config-vacuum#autovacuum-worker-slots-integer-autovacuum-worker-slots-configuration-parameter) to specify the maximum number of background workers (Nathan Bossart) [](https://postgr.es/c/c758119e5)

    With this variable set, [autovacuum_max_workers (integer)
       
        autovacuum_max_workers configuration parameter](braised:ref/runtime-config-vacuum#autovacuum-max-workers-integer-autovacuum-max-workers-configuration-parameter) can be adjusted at runtime up to this maximum without a server restart.

-   Allow specification of the fixed number of dead tuples that will trigger an [autovacuum](#autovacuum) (Nathan Bossart, Frédéric Yhuel) [](https://postgr.es/c/306dc520b)

    The server variable is [autovacuum_vacuum_max_threshold (integer)
       
        autovacuum_vacuum_max_threshold
        configuration parameter](braised:ref/runtime-config-vacuum#autovacuum-vacuum-max-threshold-integer-autovacuum-vacuum-max-threshold-configuration-parameter). Percentages are still used for triggering.

-   Change server variable [max_files_per_process (integer)
      
       max_files_per_process configuration parameter](braised:ref/runtime-config-resource#max-files-per-process-integer-max-files-per-process-configuration-parameter) to limit only files opened by a backend (Andres Freund) [](https://postgr.es/c/adb5f85fa)

    Previously files opened by the postmaster were also counted toward this limit.

-   Add server variable [num_os_semaphores (integer)
      
       num_os_semaphores configuration parameter](braised:ref/runtime-config-preset#num-os-semaphores-integer-num-os-semaphores-configuration-parameter) to report the required number of semaphores (Nathan Bossart) [](https://postgr.es/c/0dcaea569)

    This is useful for operating system configuration.

-   Add server variable [extension_control_path (string)
      
       extension_control_path configuration parameter](braised:ref/runtime-config-client#extension-control-path-string-extension-control-path-configuration-parameter) to specify the location of extension control files (Peter Eisentraut, Matheus Alcantara) [](https://postgr.es/c/4f7f7b037) [](https://postgr.es/c/81eaaa2c4)

##### Streaming Replication and Recovery

-   Allow inactive replication slots to be automatically invalidated using server variable [idle_replication_slot_timeout (integer)
      
       idle_replication_slot_timeout configuration parameter](braised:ref/runtime-config-replication#idle-replication-slot-timeout-integer-idle-replication-slot-timeout-configuration-parameter) (Nisha Moond, Bharath Rupireddy) [](https://postgr.es/c/ac0e33136)

-   Add server variable [max_active_replication_origins (integer)
       
        max_active_replication_origins configuration parameter](braised:ref/runtime-config-replication#max-active-replication-origins-integer-max-active-replication-origins-configuration-parameter) to control the maximum active replication origins (Euler Taveira) [](https://postgr.es/c/04ff636cb)

    This was previously controlled by [max_replication_slots (integer)
       
        max_replication_slots configuration parameter](braised:ref/runtime-config-replication#max-replication-slots-integer-max-replication-slots-configuration-parameter), but this new setting allows a higher origin count in cases where fewer slots are required.

##### [Logical Replication](#logical-replication)

-   Allow the values of [generated columns](#sql-createtable-parms-generated-stored) to be logically replicated (Shubham Khanna, Vignesh C, Zhijie Hou, Shlok Kyal, Peter Smith) [](https://postgr.es/c/745217a05) [](https://postgr.es/c/7054186c4) [](https://postgr.es/c/87ce27de6) [](https://postgr.es/c/6252b1eaf)

    If the publication specifies a column list, all specified columns, generated and non-generated, are published. Without a specified column list, publication option `publish_generated_columns` controls whether generated columns are published. Previously generated columns were not replicated and the subscriber had to compute the values if possible; this is particularly useful for non-PostgreSQL subscribers which lack such a capability.

-   Change the default [CREATE SUBSCRIPTION](braised:ref/sql-createsubscription) streaming option from `off` to `parallel` (Vignesh C) [](https://postgr.es/c/1bf1140be)

-   Allow [ALTER SUBSCRIPTION](braised:ref/sql-altersubscription) to change the replication slot\'s two-phase commit behavior (Hayato Kuroda, Ajin Cherian, Amit Kapila, Zhijie Hou) [](https://postgr.es/c/1462aad2e) [](https://postgr.es/c/4868c96bc)

-   Log [conflicts](#hot-standby-conflict) while applying logical replication changes (Zhijie Hou, Nisha Moond) [](https://postgr.es/c/9758174e2) [](https://postgr.es/c/edcb71258) [](https://postgr.es/c/640178c92) [](https://postgr.es/c/6c2b5edec) [](https://postgr.es/c/73eba5004)

    Also report in new columns of [pg_stat_subscription_stats](#monitoring-pg-stat-subscription-stats).

#### Utility Commands

-   Allow [generated columns](#sql-createtable-parms-generated-stored) to be virtual, and make them the default (Peter Eisentraut, Jian He, Richard Guo, Dean Rasheed) [](https://postgr.es/c/83ea6c540) [](https://postgr.es/c/cdc168ad4) [](https://postgr.es/c/1e4351af3)

    Virtual generated columns generate their values when the columns are read, not written. The write behavior can still be specified via the `STORED` option.

-   Add `OLD`/`NEW` support to [`RETURNING`](#dml-returning) in DML queries (Dean Rasheed) [](https://postgr.es/c/80feb727c)

    Previously `RETURNING` only returned new values for [INSERT](braised:ref/sql-insert) and [UPDATE](braised:ref/sql-update), and old values for [DELETE](braised:ref/sql-delete); [MERGE](braised:ref/sql-merge) would return the appropriate value for the internal query executed. This new syntax allows the `RETURNING` list of `INSERT`/`UPDATE`/`DELETE`/`MERGE` to explicitly return old and new values by using the special aliases `old` and `new`. These aliases can be renamed to avoid identifier conflicts.

-   Allow foreign tables to be created like existing local tables (Zhang Mingli) [](https://postgr.es/c/302cf1575)

    The syntax is [`CREATE FOREIGN TABLE ... LIKE`](#sql-createforeigntable).

-   Allow [`LIKE`](#functions-like) with [nondeterministic collations](#collation-nondeterministic) (Peter Eisentraut) [](https://postgr.es/c/85b7efa1c)

-   Allow text position search functions with nondeterministic collations (Peter Eisentraut) [](https://postgr.es/c/329304c90)

    These used to generate an error.

-   Add builtin collation provider [`PG_UNICODE_FAST`](#locale-providers) (Jeff Davis) [](https://postgr.es/c/d3d098316)

    This locale supports case mapping, but sorts in code point order, not natural language order.

-   Allow [VACUUM](braised:ref/sql-vacuum) and [ANALYZE](braised:ref/sql-analyze) to process partitioned tables without processing their children (Michael Harris) [](https://postgr.es/c/62ddf7ee9)

    This is enabled with the new `ONLY` option. This is useful since autovacuum does not process partitioned tables, just its children.

-   Add functions to modify per-relation and per-column optimizer statistics (Corey Huinker) [](https://postgr.es/c/e839c8ecc) [](https://postgr.es/c/d32d14639) [](https://postgr.es/c/650ab8aaf)

    The functions are [`pg_restore_relation_stats()`](#functions-admin-statsmod), `pg_restore_attribute_stats()`, `pg_clear_relation_stats()`, and `pg_clear_attribute_stats()`.

-   Add server variable [file_copy_method (enum)
      
       file_copy_method configuration parameter](braised:ref/runtime-config-resource#file-copy-method-enum-file-copy-method-configuration-parameter) to control the file copying method (Nazir Bilal Yavuz) [](https://postgr.es/c/f78ca6f3e)

    This controls whether [`CREATE DATABASE ... STRATEGY=FILE_COPY`](#sql-createdatabase) and [`ALTER DATABASE ... SET TABLESPACE`](#sql-alterdatabase) uses file copy or clone.

##### [Constraints](#ddl-constraints)

-   Allow the specification of non-overlapping [`PRIMARY KEY`](#sql-createtable-parms-primary-key), [`UNIQUE`](#sql-createtable-parms-unique), and [foreign key](#sql-createtable-parms-references) constraints (Paul A. Jungwirth) [](https://postgr.es/c/fc0438b4e) [](https://postgr.es/c/89f908a6d)

    This is specified by `WITHOUT OVERLAPS` for `PRIMARY KEY` and `UNIQUE`, and by `PERIOD` for foreign keys, all applied to the last specified column.

-   Allow [`CHECK`](#sql-createtable-parms-check) and [foreign key](#sql-createtable-parms-references) constraints to be specified as `NOT ENFORCED` (Amul Sul) [](https://postgr.es/c/ca87c415e) [](https://postgr.es/c/eec0040c4)

    This also adds column [pg_constraint](#catalog-pg-constraint).conenforced.

-   Require [primary/foreign key](#sql-createtable-parms-references) relationships to use either deterministic collations or the the same nondeterministic collations (Peter Eisentraut) [](https://postgr.es/c/9321d2fdf)

    The restore of a [pg_dump](braised:ref/app-pgdump), also used by [pg_upgrade](braised:ref/pgupgrade), will fail if these requirements are not met; schema changes must be made for these upgrade methods to succeed.

-   Store column [`NOT NULL`](#sql-createtable-parms-not-null) specifications in [pg_constraint](#catalog-pg-constraint) (Álvaro Herrera, Bernd Helmle) [](https://postgr.es/c/14e87ffa5) [](https://postgr.es/c/81ce602d4)

    This allows names to be specified for `NOT NULL` constraint. This also adds `NOT NULL` constraints to foreign tables and `NOT NULL` inheritance control to local tables.

-   Allow [ALTER TABLE](braised:ref/sql-altertable) to set the `NOT VALID` attribute of `NOT NULL` constraints (Rushabh Lathia, Jian He) [](https://postgr.es/c/a379061a2)

-   Allow modification of the inheritability of `NOT NULL` constraints (Suraj Kharage, Álvaro Herrera) [](https://postgr.es/c/f4e53e10b) [](https://postgr.es/c/4a02af8b1)

    The syntax is [`ALTER TABLE ... ALTER CONSTRAINT ... [NO] INHERIT`](#sql-altertable).

-   Allow `NOT VALID` foreign key constraints on partitioned tables (Amul Sul) [](https://postgr.es/c/b663b9436)

-   Allow [dropping](#sql-altertable-desc-drop-constraint) of constraints `ONLY` on partitioned tables (Álvaro Herrera) [](https://postgr.es/c/4dea33ce7)

    This was previously erroneously prohibited.

##### [COPY](braised:ref/sql-copy)

-   Add `REJECT_LIMIT` to control the number of invalid rows `COPY FROM` can ignore (Atsushi Torikoshi) [](https://postgr.es/c/4ac2a9bec)

    This is available when `ON_ERROR = 'ignore'`.

-   Allow `COPY TO` to copy rows from populated materialized views (Jian He) [](https://postgr.es/c/534874fac)

-   Add `COPY` `LOG_VERBOSITY` level `silent` to suppress log output of ignored rows (Atsushi Torikoshi) [](https://postgr.es/c/e7834a1a2)

    This new level suppresses output for discarded input rows when `on_error = 'ignore'`.

-   Disallow `COPY FREEZE` on foreign tables (Nathan Bossart) [](https://postgr.es/c/401a6956f)

    Previously, the `COPY` worked but the `FREEZE` was ignored, so disallow this command.

##### [EXPLAIN](braised:ref/sql-explain)

-   Automatically include `BUFFERS` output in `EXPLAIN ANALYZE` (Guillaume Lelarge, David Rowley) [](https://postgr.es/c/c2a4078eb)

-   Add full WAL buffer count to `EXPLAIN (WAL)` output (Bertrand Drouvot) [](https://postgr.es/c/320545bfc)

-   In `EXPLAIN ANALYZE`, report the number of index lookups used per index scan node (Peter Geoghegan) [](https://postgr.es/c/0fbceae84)

-   Modify `EXPLAIN` to output fractional row counts (Ibrar Ahmed, Ilia Evdokimov, Robert Haas) [](https://postgr.es/c/ddb17e387) [](https://postgr.es/c/95dbd827f)

-   Add memory and disk usage details to `Material`, `Window Aggregate`, and common table expression nodes to `EXPLAIN` output (David Rowley, Tatsuo Ishii) [](https://postgr.es/c/1eff8279d) [](https://postgr.es/c/53abb1e0e) [](https://postgr.es/c/95d6e9af0) [](https://postgr.es/c/40708acd6)

-   Add details about window function arguments to `EXPLAIN` output (Tom Lane) [](https://postgr.es/c/8b1b34254)

-   Add `Parallel Bitmap Heap Scan` worker cache statistics to `EXPLAIN ANALYZE` (David Geier, Heikki Linnakangas, Donghang Lin, Alena Rybakina, David Rowley) [](https://postgr.es/c/5a1e6df3b)

-   Indicate disabled nodes in `EXPLAIN ANALYZE` output (Robert Haas, David Rowley, Laurenz Albe) [](https://postgr.es/c/c01743aa4) [](https://postgr.es/c/161320b4b) [](https://postgr.es/c/84b8fccbe)

#### Data Types

-   Improve [Unicode](#collation-managing-standard) full case mapping and conversion (Jeff Davis) [](https://postgr.es/c/4e7f62bc3) [](https://postgr.es/c/286a365b9)

    This adds the ability to do conditional and title case mapping, and case map single characters to multiple characters.

-   Allow [`jsonb`](#datatype-json) `null` values to be cast to scalar types as `NULL` (Tom Lane) [](https://postgr.es/c/a5579a90a)

    Previously such casts generated an error.

-   Add optional parameter to `json{b}_strip_nulls` to allow removal of null array elements (Florents Tselai) [](https://postgr.es/c/4603903d2)

-   Add function `array_sort()` which sorts an array\'s first dimension (Junwang Zhao, Jian He) [](https://postgr.es/c/6c12ae09f)

-   Add function `array_reverse()` which reverses an array\'s first dimension (Aleksander Alekseev) [](https://postgr.es/c/49d6c7d8d)

-   Add function [`reverse()`](#functions-string-other) to reverse bytea bytes (Aleksander Alekseev) [](https://postgr.es/c/0697b2390)

-   Allow casting between integer types and [`bytea`](#datatype-binary) (Aleksander Alekseev) [](https://postgr.es/c/6da469bad)

    The integer values are stored as `bytea` two\'s complement values.

-   Update Unicode data to [Unicode](#collation-managing-standard) 16.0.0 (Peter Eisentraut) [](https://postgr.es/c/82a46cca9)

-   Add full text search [stemming](#textsearch-snowball-dictionary) for Estonian (Tom Lane) [](https://postgr.es/c/b464e51ab)

-   Improve the [`XML`](#datatype-xml) error codes to more closely match the SQL standard (Tom Lane) [](https://postgr.es/c/cd838e200)

    These errors are reported via [`SQLSTATE`](#errcodes-appendix).

#### Functions

-   Add function [`casefold()`](#functions-string-other) to allow for more sophisticated case-insensitive matching (Jeff Davis) [](https://postgr.es/c/bfc599206)

    This allows more accurate comparisons, i.e., a character can have multiple upper or lower case equivalents, or upper or lower case conversion changes the number of characters.

-   Allow `MIN()`/`MAX()` aggregates on arrays and composite types (Aleksander Alekseev, Marat Buharov) [](https://postgr.es/c/a0f1fce80) [](https://postgr.es/c/2d24fd942)

-   Add a `WEEK` option to [`EXTRACT()`](#functions-datetime-extract) (Tom Lane) [](https://postgr.es/c/6be39d77a)

-   Improve the output `EXTRACT(QUARTER ...)` for negative values (Tom Lane) [](https://postgr.es/c/6be39d77a)

-   Add roman numeral support to `to_number()` (Hunaid Sohail) [](https://postgr.es/c/172e6b3ad)

    This is accessed via the `RN` pattern.

-   Add [`UUID`](#datatype-uuid) version 7 generation function [`uuidv7()`](#func_uuid_gen_table) (Andrey Borodin) [](https://postgr.es/c/78c5e141e)

    This `UUID` value is temporally sortable. Function alias [`uuidv4()`](#func_uuid_gen_table) has been added to explicitly generate version 4 UUIDs.

-   Add functions [`crc32()`](#functions-binarystring-other) and [`crc32c()`](#functions-binarystring-other) to compute CRC values (Aleksander Alekseev) [](https://postgr.es/c/760162fed)

-   Add math functions `gamma()` and `lgamma()` (Dean Rasheed) [](https://postgr.es/c/a3b6dfd41)

-   Allow `=>` syntax for named cursor arguments in [PL/pgSQL](#plpgsql) (Pavel Stehule) [](https://postgr.es/c/246dedc5d)

    We previously only accepted `:=`.

-   Allow [`regexp_match[es]()`](#functions-posix-regexp)/[`regexp_like()`](#functions-posix-regexp)/[`regexp_replace()`](#functions-posix-regexp)/[`regexp_count()`](#functions-posix-regexp)/[`regexp_instr()`](#functions-posix-regexp)/[`regexp_substr()`](#functions-posix-regexp)/[`regexp_split_to_table()`](#functions-posix-regexp)/[`regexp_split_to_array()`](#functions-posix-regexp) to use named arguments (Jian He) [](https://postgr.es/c/580f8727c)

#### [Libpq](#libpq)

-   Add function [`PQfullProtocolVersion()`](#libpq-PQfullProtocolVersion) to report the full, including minor, protocol version number (Jacob Champion, Jelte Fennema-Nio) [](https://postgr.es/c/cdb6b0fdb)

-   Add libpq connection [parameters](#libpq-connect-ssl-max-protocol-version) and [environment variables](#libpq-envars) to specify the minimum and maximum acceptable protocol version for connections (Jelte Fennema-Nio) [](https://postgr.es/c/285613c60) [](https://postgr.es/c/507034910)

-   Report [search_path (string)
      
       search_path configuration parameter
      
      pathfor schemas](braised:ref/runtime-config-client#search-path-string-search-path-configuration-parameter-pathfor-schemas) changes to the client (Alexander Kukushkin, Jelte Fennema-Nio, Tomas Vondra) [](https://postgr.es/c/28a1121fd) [](https://postgr.es/c/0d06a7eac)

-   Add [`PQtrace()`](#libpq-PQtrace) output for all message types, including authentication (Jelte Fennema-Nio) [](https://postgr.es/c/ea92f3a0a) [](https://postgr.es/c/a5c6b8f22) [](https://postgr.es/c/b8b3f861f) [](https://postgr.es/c/e87c14b19) [](https://postgr.es/c/7adec2d5f)

-   Add libpq connection parameter [`sslkeylogfile`](#libpq-connect-sslkeylogfile) which dumps out SSL key material (Abhishek Chanda, Daniel Gustafsson) [](https://postgr.es/c/2da74d8d6)

    This is useful for debugging.

-   Modify some libpq function signatures to use `int64_t` (Thomas Munro) [](https://postgr.es/c/3c86223c9)

    These previously used `pg_int64`, which is now deprecated.

#### [psql](braised:ref/app-psql)

-   Allow psql to parse, bind, and close named prepared statements (Anthonin Bonnefoy, Michael Paquier) [](https://postgr.es/c/d55322b0d) [](https://postgr.es/c/fc39b286a)

    This is accomplished with new commands [`\parse`](#app-psql-meta-command-parse), [`\bind_named`](#app-psql-meta-command-bind-named), and [`\close_prepared`](#app-psql-meta-command-close-prepared).

-   Add psql backslash commands to allowing issuance of pipeline queries (Anthonin Bonnefoy) [](https://postgr.es/c/41625ab8e) [](https://postgr.es/c/17caf6644) [](https://postgr.es/c/2cce0fe44)

    The new commands are [`\startpipeline`](#app-psql-meta-command-pipeline), `\syncpipeline`, `\sendpipeline`, `\endpipeline`, `\flushrequest`, `\flush`, and `\getresults`.

-   Allow adding pipeline status to the psql prompt and add related state variables (Anthonin Bonnefoy) [](https://postgr.es/c/3ce357584)

    The new prompt character is `%P` and the new psql variables are [`PIPELINE_SYNC_COUNT`](#app-psql-variables-pipeline-sync-count), [`PIPELINE_COMMAND_COUNT`](#app-psql-variables-pipeline-command-count), and [`PIPELINE_RESULT_COUNT`](#app-psql-variables-pipeline-result-count).

-   Allow adding the connection service name to the psql prompt or access it via psql variable (Michael Banck) [](https://postgr.es/c/477728b5d)

-   Add psql option to use expanded mode on all list commands (Dean Rasheed) [](https://postgr.es/c/00f4c2959)

    Adding backslash suffix `x` enables this.

-   Change psql\'s [\conninfo](braised:ref/app-psql#conninfo) to use tabular format and include more information (Álvaro Herrera, Maiquel Grassi, Hunaid Sohail) [](https://postgr.es/c/bba2fbc62)

-   Add function\'s leakproof indicator to psql\'s [`\df+`](#app-psql-meta-command-df-lc), `\do+`, `\dAo+`, and `\dC+` outputs (Yugo Nagata) [](https://postgr.es/c/2355e5111)

-   Add access method details for partitioned relations in [`\dP+`](#app-psql-meta-command-dp-uc) (Justin Pryzby) [](https://postgr.es/c/978f38c77)

-   Add `default_version` to the psql [`\dx`](#app-psql-meta-command-dx-lc) extension output (Magnus Hagander) [](https://postgr.es/c/d696406a9)

-   Add psql variable [WATCH_INTERVAL](braised:ref/app-psql#watch-interval) to set the default [`\watch`](#app-psql-meta-command-watch) wait time (Daniel Gustafsson) [](https://postgr.es/c/1a759c832)

#### Server Applications

-   Change [initdb](braised:ref/app-initdb) to default to enabling checksums (Greg Sabino Mullane) [](https://postgr.es/c/983a588e0) [](https://postgr.es/c/04bec894a)

    The new initdb option `--no-data-checksums` disables checksums.

-   Add initdb option `--no-sync-data-files` to avoid syncing heap/index files (Nathan Bossart) [](https://postgr.es/c/cf131fa94)

    initdb option `--no-sync` is still available to avoid syncing any files.

-   Add [vacuumdb](braised:ref/app-vacuumdb) option `--missing-stats-only` to compute only missing optimizer statistics (Corey Huinker, Nathan Bossart) [](https://postgr.es/c/edba754f0) [](https://postgr.es/c/987910502)

    This option can only be run by superusers and can only be used with options `--analyze-only` and `--analyze-in-stages`.

-   Add [pg_combinebackup](braised:ref/app-pgcombinebackup) option `-k`/`--link` to enable hard linking (Israel Barth Rubio, Robert Haas) [](https://postgr.es/c/99aeb8470)

    Only some files can be hard linked. This should not be used if the backups will be used independently.

-   Allow [pg_verifybackup](braised:ref/app-pgverifybackup) to verify tar-format backups (Amul Sul) [](https://postgr.es/c/8dfd31290)

-   If [pg_rewind](braised:ref/app-pgrewind)\'s `--source-server` specifies a database name, use it in `--write-recovery-conf` output (Masahiko Sawada) [](https://postgr.es/c/4ecdd4110)

-   Add [pg_resetwal](braised:ref/app-pgresetwal) option `--char-signedness` to change the default `char` signedness (Masahiko Sawada) [](https://postgr.es/c/30666d185)

##### [pg_dump](#app-pgdump)/[pg_dumpall](#app-pg-dumpall)/[pg_restore](#app-pgrestore)

-   Add [pg_dump](braised:ref/app-pgdump) option `--statistics` (Jeff Davis) [](https://postgr.es/c/bde2fb797) [](https://postgr.es/c/a3e8dc143)

-   Add pg_dump and [pg_dumpall](braised:ref/app-pg-dumpall) option `--sequence-data` to dump sequence data that would normally be excluded (Nathan Bossart) [](https://postgr.es/c/9c49f0e8c) [](https://postgr.es/c/acea3fc49)

-   Add [pg_dump](braised:ref/app-pgdump), [pg_dumpall](braised:ref/app-pg-dumpall), and [pg_restore](braised:ref/app-pgrestore) options `--statistics-only`, `--no-statistics`, `--no-data`, and `--no-schema` (Corey Huinker, Jeff Davis) [](https://postgr.es/c/1fd1bd871)

-   Add option `--no-policies` to disable row level security policy processing in [pg_dump](braised:ref/app-pgdump), [pg_dumpall](braised:ref/app-pg-dumpall), [pg_restore](braised:ref/app-pgrestore) (Nikolay Samokhvalov) [](https://postgr.es/c/cd3c45125)

    This is useful for migrating to systems with different policies.

##### [pg_upgrade](braised:ref/pgupgrade)

-   Allow pg_upgrade to preserve optimizer statistics (Corey Huinker, Jeff Davis, Nathan Bossart) [](https://postgr.es/c/1fd1bd871) [](https://postgr.es/c/c9d502eb6) [](https://postgr.es/c/d5f1b6a75) [](https://postgr.es/c/1fd1bd871)

    Extended statistics are not preserved. Also add pg_upgrade option `--no-statistics` to disable statistics preservation.

-   Allow pg_upgrade to process database checks in parallel (Nathan Bossart) [](https://postgr.es/c/40e2e5e92) [](https://postgr.es/c/6d3d2e8e5) [](https://postgr.es/c/7baa36de5) [](https://postgr.es/c/46cad8b31) [](https://postgr.es/c/6ab8f27bc) [](https://postgr.es/c/bbf83cab9) [](https://postgr.es/c/9db3018cf) [](https://postgr.es/c/c34eabfbb) [](https://postgr.es/c/cf2f82a37) [](https://postgr.es/c/f93f5f7b9) [](https://postgr.es/c/c880cf258)

    This is controlled by the existing `--jobs` option.

-   Add pg_upgrade option `--swap` to swap directories rather than copy, clone, or link files (Nathan Bossart) [](https://postgr.es/c/626d7236b)

    This mode is potentially the fastest.

-   Add pg_upgrade option `--set-char-signedness` to set the default `char` signedness of new cluster (Masahiko Sawada) [](https://postgr.es/c/a8238f87f) [](https://postgr.es/c/1aab68059)

    This is to handle cases where a pre-PostgreSQL 18 cluster\'s default CPU signedness does not match the new cluster.

##### Logical Replication Applications

-   Add [pg_createsubscriber](braised:ref/app-pgcreatesubscriber) option `--all` to create logical replicas for all databases (Shubham Khanna) [](https://postgr.es/c/fb2ea12f4)

-   Add pg_createsubscriber option `--clean` to remove publications (Shubham Khanna) [](https://postgr.es/c/e5aeed4b8) [](https://postgr.es/c/60dda7bbc)

-   Add pg_createsubscriber option `--enable-two-phase` to enable prepared transactions (Shubham Khanna) [](https://postgr.es/c/e117cfb2f)

-   Add [pg_recvlogical](braised:ref/app-pgrecvlogical) option `--enable-failover` to specify failover slots (Hayato Kuroda) [](https://postgr.es/c/cf2655a90)

    Also add option `--enable-two-phase` as a synonym for `--two-phase`, and deprecate the latter.

-   Allow pg_recvlogical `--drop-slot` to work without `--dbname` (Hayato Kuroda) [](https://postgr.es/c/c68100aa4)

#### Source Code

-   Separate the loading and running of [injection points](#xfunc-addin-injection-points) (Michael Paquier, Heikki Linnakangas) [](https://postgr.es/c/4b211003e) [](https://postgr.es/c/a0a5869a8)

    Injection points can now be created, but not run, via [`INJECTION_POINT_LOAD()`](#xfunc-addin-injection-points), and such injection points can be run via [`INJECTION_POINT_CACHED()`](#xfunc-addin-injection-points).

-   Support runtime arguments in injection points (Michael Paquier) [](https://postgr.es/c/371f2db8b)

-   Allow inline injection point test code with [`IS_INJECTION_POINT_ATTACHED()`](#xfunc-addin-injection-points) (Heikki Linnakangas) [](https://postgr.es/c/20e0e7da9)

-   Improve the performance of processing long [`JSON`](#datatype-json) strings using SIMD (Single Instruction Multiple Data) (David Rowley) [](https://postgr.es/c/ca6fde922)

-   Speed up CRC32C calculations using x86 AVX-512 instructions (Raghuveer Devulapalli, Paul Amonson) [](https://postgr.es/c/3c6e8c123)

-   Add ARM Neon and SVE CPU intrinsics for popcount (integer bit counting) (Chiranmoy Bhattacharya, Devanga Susmitha, Rama Malladi) [](https://postgr.es/c/6be53c276) [](https://postgr.es/c/519338ace)

-   Improve the speed of numeric multiplication and division (Joel Jacobson, Dean Rasheed) [](https://postgr.es/c/ca481d3c9) [](https://postgr.es/c/c4e44224c) [](https://postgr.es/c/8dc28d7eb) [](https://postgr.es/c/9428c001f)

-   Add configure option [`--with-libnuma`](#configure-option-with-libnuma) to enable NUMA awareness (Jakub Wartak, Bertrand Drouvot) [](https://postgr.es/c/65c298f61) [](https://postgr.es/c/8cc139bec) [](https://postgr.es/c/ba2a3c230)

    The function `pg_numa_available()` reports on NUMA awareness, and system views [pg_shmem_allocations_numa](#view-pg-shmem-allocations-numa) and [pg_buffercache_numa](#pgbuffercache-pg-buffercache-numa) which report on shared memory distribution across NUMA nodes.

-   Add [TOAST](#storage-toast) table to [pg_index](#catalog-pg-index) to allow for very large expression indexes (Nathan Bossart) [](https://postgr.es/c/b52c4fc3c)

-   Remove column [pg_attribute](#catalog-pg-attribute).attcacheoff (David Rowley) [](https://postgr.es/c/02a8d0c45)

-   Add column [pg_class](#catalog-pg-class).relallfrozen (Melanie Plageman) [](https://postgr.es/c/99f8f3fbb)

-   Add [amgettreeheight](#indexam), `amconsistentequality`, and `amconsistentordering` to the index access method API (Mark Dilger) [](https://postgr.es/c/56fead44d) [](https://postgr.es/c/af4002b38)

-   Add GiST support function [`stratnum()`](#gist-extensibility) (Paul A. Jungwirth) [](https://postgr.es/c/7406ab623)

-   Record the default CPU signedness of `char` in [pg_controldata](braised:ref/app-pgcontroldata) (Masahiko Sawada) [](https://postgr.es/c/44fe30fda)

-   Add support for Python \"Limited API\" in [PL/Python](#plpython) (Peter Eisentraut) [](https://postgr.es/c/72a3d0462) [](https://postgr.es/c/0793ab810)

    This helps prevent problems caused by Python 3.x version mismatches.

-   Change the minimum supported Python version to 3.6.8 (Jacob Champion) [](https://postgr.es/c/45363fca6)

-   Remove support for OpenSSL versions older than 1.1.1 (Daniel Gustafsson) [](https://postgr.es/c/a70e01d43) [](https://postgr.es/c/6c66b7443)

-   If LLVM is enabled, require version 14 or later (Thomas Munro) [](https://postgr.es/c/972c2cd28)

-   Add macro [`PG_MODULE_MAGIC_EXT`](#functions-info) to allow extensions to report their name and version (Andrei Lepikhov) [](https://postgr.es/c/9324c8c58)

    This information can be access via the new function `pg_get_loaded_modules()`.

-   Document that [`SPI_connect()`](#spi-spi-connect)/[`SPI_connect_ext()`](#spi-spi-connect) always returns success (`SPI_OK_CONNECT`) (Stepan Neretin) [](https://postgr.es/c/218527d01)

    Errors are always reported via `ereport()`.

-   Add [documentation section](#xfunc-api-abi-stability-guidance) about API and ABI compatibility (David Wheeler, Peter Eisentraut) [](https://postgr.es/c/e54a42ac9)

-   Remove the experimental designation of Meson builds on `Windows` (Aleksander Alekseev) [](https://postgr.es/c/5afaba629)

-   Remove configure options `--disable-spinlocks` and `--disable-atomics` (Thomas Munro) [](https://postgr.es/c/e25626677) [](https://postgr.es/c/813852613)

    Thirty-two-bit atomic operations are now required.

-   Remove support for the HPPA/PA-RISC architecture (Tom Lane) [](https://postgr.es/c/edadeb071)

#### Additional Modules

-   Add extension [F.28. pg_logicalinspect — logical decoding components inspection](braised:ref/pglogicalinspect) to inspect logical snapshots (Bertrand Drouvot) [](https://postgr.es/c/7cdfeee32)

-   Add extension [F.29. pg_overexplain — allow EXPLAIN to dump even more details](braised:ref/pgoverexplain) which adds debug details to [`EXPLAIN`](#sql-explain) output (Robert Haas) [](https://postgr.es/c/8d5ceb113)

-   Add output columns to [`postgres_fdw_get_connections()`](#postgres-fdw-functions) (Hayato Kuroda, Sagar Dilip Shedge) [](https://postgr.es/c/c297a47c5) [](https://postgr.es/c/857df3cef) [](https://postgr.es/c/4f08ab554) [](https://postgr.es/c/fe186bda7)

    New output column used_in_xact indicates if the foreign data wrapper is being used by a current transaction, closed indicates if it is closed, user_name indicates the user name, and remote_backend_pid indicates the remote backend process identifier.

-   Allow [SCRAM](#auth-password) authentication from the client to be passed to [F.38. postgres_fdw — access data stored in external PostgreSQL servers](braised:ref/postgres-fdw) servers (Matheus Alcantara, Peter Eisentraut) [](https://postgr.es/c/761c79508)

    This avoids storing postgres_fdw authentication information in the database, and is enabled with the postgres_fdw [`use_scram_passthrough`](#postgres-fdw-option-use-scram-passthrough) connection option. libpq uses new connection parameters [scram_client_key](braised:ref/libpq-connect#scram-client-key) and [scram_server_key](braised:ref/libpq-connect#scram-server-key).

-   Allow SCRAM authentication from the client to be passed to [F.11. dblink — connect to other PostgreSQL databases](braised:ref/dblink) servers (Matheus Alcantara) [](https://postgr.es/c/3642df265)

-   Add `on_error` and `log_verbosity` options to [F.15. file_fdw — access data files in the server's file system](braised:ref/file-fdw) (Atsushi Torikoshi) [](https://postgr.es/c/a1c4c8a9e)

    These control how file_fdw handles and reports invalid file rows.

-   Add `reject_limit` to control the number of invalid rows file_fdw can ignore (Atsushi Torikoshi) [](https://postgr.es/c/6c8f67032)

    This is active when `ON_ERROR = 'ignore'`.

-   Add configurable variable `min_password_length` to [F.24. passwordcheck — verify password strength](braised:ref/passwordcheck) (Emanuele Musella, Maurizio Boriani) [](https://postgr.es/c/f7e1b3828)

    This controls the minimum password length.

-   Have [pgbench](braised:ref/pgbench) report the number of failed, retried, or skipped transactions in per-script reports (Yugo Nagata) [](https://postgr.es/c/cae0f3c40)

-   Add [F.20. isn — data types for international standard numbers (ISBN, EAN, UPC, etc.)](braised:ref/isn) server variable `weak` to control invalid check digit acceptance (Viktor Holmberg) [](https://postgr.es/c/448904423)

    This was previously only controlled by function [`isn_weak()`](#isn-functions).

-   Allow values to be sorted to speed [F.8. btree_gist — GiST operator classes with B-tree behavior](braised:ref/btree-gist) index builds (Bernd Helmle, Andrey Borodin) [](https://postgr.es/c/e4309f73f)

-   Add [F.1. amcheck — tools to verify table and index consistency](braised:ref/amcheck) check function [`gin_index_check()`](#amcheck-functions) to verify `GIN` indexes (Grigory Kryachko, Heikki Linnakangas, Andrey Borodin) [](https://postgr.es/c/14ffaece0)

-   Add functions [`pg_buffercache_evict_relation()`](#pgbuffercache-pg-buffercache-evict-relation) and [`pg_buffercache_evict_all()`](#pgbuffercache-pg-buffercache-evict-all) to evict unpinned shared buffers (Nazir Bilal Yavuz) [](https://postgr.es/c/dcf7e1697)

    The existing function [`pg_buffercache_evict()`](#pgbuffercache-pg-buffercache-evict) now returns the buffer flush status.

-   Allow extensions to install custom [EXPLAIN](braised:ref/sql-explain) options (Robert Haas, Sami Imseih) [](https://postgr.es/c/c65bc2e1d) [](https://postgr.es/c/4fd02bf7c) [](https://postgr.es/c/50ba65e73)

-   Allow extensions to use the server\'s cumulative statistics API (Michael Paquier) [](https://postgr.es/c/7949d9594) [](https://postgr.es/c/2eff9e678)

##### [F.32. pg_stat_statements — track statistics of SQL planning and execution](braised:ref/pgstatstatements)

-   Allow the queries of [CREATE TABLE AS](braised:ref/sql-createtableas) and [DECLARE](braised:ref/sql-declare) to be tracked by pg_stat_statements (Anthonin Bonnefoy) [](https://postgr.es/c/6b652e6ce)

    They are also now assigned query ids.

-   Allow the parameterization of [SET](braised:ref/sql-set) values in pg_stat_statements (Greg Sabino Mullane, Michael Paquier) [](https://postgr.es/c/dc6851596)

    This reduces the bloat caused by `SET` statements with differing constants.

-   Add [pg_stat_statements](#pgstatstatements-pg-stat-statements) columns to report parallel activity (Guillaume Lelarge) [](https://postgr.es/c/cf54a2c00)

    The new columns are parallel_workers_to_launch and parallel_workers_launched.

-   Add pg_stat_statements.wal_buffers_full to report full WAL buffers (Bertrand Drouvot) [](https://postgr.es/c/ce5bcc4a9)

##### [F.26. pgcrypto — cryptographic functions](braised:ref/pgcrypto)

-   Add pgcrypto algorithms [`sha256crypt`](#pgcrypto-crypt-algorithms) and [`sha512crypt`](#pgcrypto-crypt-algorithms) (Bernd Helmle) [](https://postgr.es/c/749a9e20c)

-   Add [CFB](#pgcrypto-raw-enc-funcs) mode to pgcrypto encryption and decryption (Umar Hayat) [](https://postgr.es/c/9ad1b3d01)

-   Add function [`fips_mode()`](#pgcrypto-openssl-support-funcs) to report the server\'s FIPS mode (Daniel Gustafsson) [](https://postgr.es/c/924d89a35)

-   Add pgcrypto server variable [`builtin_crypto_enabled`](#pgcrypto-configuration-parameters-builtin_crypto_enabled) to allow disabling builtin non-FIPS mode cryptographic functions (Daniel Gustafsson, Joe Conway) [](https://postgr.es/c/035f99cbe)

    This is useful for guaranteeing FIPS mode behavior.

### Acknowledgments

The following individuals (in alphabetical order) have contributed to this release as patch authors, committers, reviewers, testers, or reporters of issues.

Abhishek Chanda

Adam Guo

Adam Rauch

Aidar Imamov

Ajin Cherian

Alastair Turner

Alec Cozens

Aleksander Alekseev

Alena Rybakina

Alex Friedman

Alex Richman

Alexander Alehin

Alexander Borisov

Alexander Korotkov

Alexander Kozhemyakin

Alexander Kukushkin

Alexander Kuzmenkov

Alexander Kuznetsov

Alexander Lakhin

Alexander Pyhalov

Alexandra Wang

Alexey Dvoichenkov

Alexey Makhmutov

Alexey Shishkin

Ali Akbar

Álvaro Herrera

Álvaro Mongil

Amit Kapila

Amit Langote

Amul Sul

Andreas Karlsson

Andreas Scherbaum

Andreas Ulbrich

Andrei Lepikhov

Andres Freund

Andrew

Andrew Bille

Andrew Dunstan

Andrew Jackson

Andrew Kane

Andrew Watkins

Andrey Borodin

Andrey Chudnovsky

Andrey Rachitskiy

Andrey Rudometov

Andy Alsup

Andy Fan

Anthonin Bonnefoy

Anthony Hsu

Anthony Leung

Anton Melnikov

Anton Voloshin

Antonin Houska

Antti Lampinen

Arseniy Mukhin

Artur Zakirov

Arun Thirupathi

Ashutosh Bapat

Asphator

Atsushi Torikoshi

Avi Weinberg

Aya Iwata

Ayush Tiwari

Ayush Vatsa

Bastien Roucariès

Ben Peachey Higdon

Benoit Lobréau

Bernd Helmle

Bernd Reiß

Bernhard Wiedemann

Bertrand Drouvot

Bertrand Mamasam

Bharath Rupireddy

Bogdan Grigorenko

Boyu Yang

Braulio Fdo Gonzalez

Bruce Momjian

Bykov Ivan

Cameron Vogt

Cary Huang

Cédric Villemain

Cees van Zeeland

ChangAo Chen

Chao Li

Chapman Flack

Charles Samborski

Chengwen Wu

Chengxi Sun

Chiranmoy Bhattacharya

Chris Gooch

Christian Charukiewicz

Christoph Berg

Christophe Courtois

Christopher Inokuchi

Clemens Ruck

Corey Huinker

Craig Milhiser

Crisp Lee

Dagfinn Ilmari Mannsåker

Daniel Elishakov

Daniel Gustafsson

Daniel Vérité

Daniel Westermann

Daniele Varrazzo

Daniil Davydov

Daria Shanina

Dave Cramer

Dave Page

David Benjamin

David Christensen

David Fiedler

David G. Johnston

David Geier

David Rowley

David Steele

David Wheeler

David Zhang

Davinder Singh

Dean Rasheed

Devanga Susmitha

Devrim Gündüz

Dian Fay

Dilip Kumar

Dimitrios Apostolou

Dipesh Dhameliya

Dmitrii Bondar

Dmitry Dolgov

Dmitry Koval

Dmitry Kovalenko

Dmitry Yurichev

Dominique Devienne

Donghang Lin

Dorjpalam Batbaatar

Drew Callahan

Duncan Sands

Dwayne Towell

Dzmitry Jachnik

Egor Chindyaskin

Egor Rogov

Emanuel Ionescu

Emanuele Musella

Emre Hasegeli

Eric Cyr

Erica Zhang

Erik Nordström

Erik Rijkers

Erik Wienhold

Erki Eessaar

Ethan Mertz

Etienne LAFARGE

Etsuro Fujita

Euler Taveira

Evan Si

Evgeniy Gorbanev

Fabio R. Sluzala

Fabrízio de Royes Mello

Feike Steenbergen

Feliphe Pozzer

Felix

Fire Emerald

Florents Tselai

Francesco Degrassi

Frank Streitzig

Frédéric Yhuel

Fredrik Widlert

Gabriele Bartolini

Gavin Panella

Geoff Winkless

George MacKerron

Gilles Darold

Grant Gryczan

Greg Burd

Greg Sabino Mullane

Greg Stark

Grigory Kryachko

Guillaume Lelarge

Gunnar Morling

Gunnar Wagner

Gurjeet Singh

Haifang Wang

Hajime Matsunaga

Hamid Akhtar

Hannu Krosing

Hari Krishna Sunder

Haruka Takatsuka

Hayato Kuroda

Heikki Linnakangas

Hironobu Suzuki

Holger Jakobs

Hubert Lubaczewski

Hugo Dubois

Hugo Zhang

Hunaid Sohail

Hywel Carver

Ian Barwick

Ibrar Ahmed

Igor Gnatyuk

Igor Korot

Ilia Evdokimov

Ilya Gladyshev

Ilyasov Ian

Imran Zaheer

Isaac Morland

Israel Barth Rubio

Ivan Kush

Jacob Brazeal

Jacob Champion

Jaime Casanova

Jakob Egger

Jakub Wartak

James Coleman

James Hunter

Jan Behrens

Japin Li

Jason Smith

Jayesh Dehankar

Jeevan Chalke

Jeff Davis

Jehan-Guillaume de Rorthais

Jelte Fennema-Nio

Jian He

Jianghua Yang

Jiao Shuntian

Jim Jones

Jim Nasby

Jingtang Zhang

Jingzhou Fu

Joe Conway

Joel Jacobson

John Hutchins

John Naylor

Jonathan Katz

Jorge Solórzano

José Villanova

Josef Šimánek

Joseph Koshakow

Julien Rouhaud

Junwang Zhao

Justin Pryzby

Kaido Vaikla

Kaimeh

Karina Litskevich

Karthik S

Kartyshov Ivan

Kashif Zeeshan

Keisuke Kuroda

Kevin Hale Boyes

Kevin K Biju

Kirill Reshke

Kirill Zdornyy

Koen De Groote

Koichi Suzuki

Koki Nakamura

Konstantin Knizhnik

Kouhei Sutou

Kuntal Ghosh

Kyotaro Horiguchi

Lakshmi Narayana Velayudam

Lars Kanis

Laurence Parry

Laurenz Albe

Lele Gaifax

Li Yong

Lilian Ontowhee

Lingbin Meng

Luboslav Špilák

Luca Vallisa

Lukas Fittl

Maciek Sakrejda

Magnus Hagander

Mahendra Singh Thalor

Mahendrakar Srinivasarao

Maiquel Grassi

Maksim Korotkov

Maksim Melnikov

Man Zeng

Marat Buharov

Marc Balmer

Marco Nenciarini

Marcos Pegoraro

Marina Polyakova

Mark Callaghan

Mark Dilger

Marlene Brandstaetter

Marlene Reiterer

Martin Rakhmanov

Masahiko Sawada

Masahiro Ikeda

Masao Fujii

Mason Mackaman

Mat Arye

Matheus Alcantara

Mats Kindahl

Matthew Gabeler-Lee

Matthew Kim

Matthew Sterrett

Matthew Woodcraft

Matthias van de Meent

Matthieu Denais

Maurizio Boriani

Max Johnson

Max Madden

Maxim Boguk

Maxim Orlov

Maximilian Chrzan

Melanie Plageman

Melih Mutlu

Mert Alev

Michael Banck

Michael Bondarenko

Michael Christofides

Michael Guissine

Michael Harris

Michaël Paquier

Michail Nikolaev

Michal Kleczek

Michel Pelletier

Mikaël Gourlaouen

Mikhail Gribkov

Mikhail Kot

Milosz Chmura

Muralikrishna Bandaru

Murat Efendioglu

Mutaamba Maasha

Naeem Akhter

Nat Makarevitch

Nathan Bossart

Navneet Kumar

Nazir Bilal Yavuz

Neil Conway

Niccolò Fei

Nick Davies

Nicolas Maus

Niek Brasa

Nikhil Raj

Nikita

Nikita Kalinin

Nikita Malakhov

Nikolay Samokhvalov

Nikolay Shaplov

Nisha Moond

Nitin Jadhav

Nitin Motiani

Noah Misch

Noboru Saito

Noriyoshi Shinoda

Ole Peder Brandtzæg

Oleg Sibiryakov

Oleg Tselebrovskiy

Olleg Samoylov

Onder Kalaci

Ondrej Navratil

Patrick Stählin

Paul Amonson

Paul Jungwirth

Paul Ramsey

Pavel Borisov

Pavel Luzanov

Pavel Nekrasov

Pavel Stehule

Peter Eisentraut

Peter Geoghegan

Peter Mittere

Peter Smith

Phil Eaton

Philipp Salvisberg

Philippe Beaudoin

Pierre Giraud

Pixian Shi

Polina Bungina

Przemyslaw Sztoch

Quynh Tran

Rafia Sabih

Raghuveer Devulapalli

Rahila Syed

Rama Malladi

Ran Benita

Ranier Vilela

Renan Alves Fonseca

Richard Guo

Richard Neill

Rintaro Ikeda

Robert Haas

Robert Treat

Robins Tharakan

Roman Zharkov

Ronald Cruz

Ronan Dunklau

Rui Zhao

Rushabh Lathia

Rustam Allakov

Ryo Kanbayashi

Ryohei Takahashi

RyotaK

Sagar Dilip Shedge

Salvatore Dipietro

Sam Gabrielsson

Sam James

Sameer Kumar

Sami Imseih

Samuel Thibault

Satyanarayana Narlapuram

Sebastian Skalacki

Senglee Choi

Sergei Kornilov

Sergey Belyashov

Sergey Dudoladov

Sergey Prokhorenko

Sergey Sargsyan

Sergey Soloviev

Sergey Tatarintsev

Shaik Mohammad Mujeeb

Shawn McCoy

Shenhao Wang

Shihao Zhong

Shinya Kato

Shlok Kyal

Shubham Khanna

Shveta Malik

Simon Riggs

Smolkin Grigory

Sofia Kopikova

Song Hongyu

Song Jinzhou

Soumyadeep Chakraborty

Sravan Kumar

Srinath Reddy

Stan Hu

Stepan Neretin

Stephen Fewer

Stephen Frost

Steve Chavez

Steven Niu

Suraj Kharage

Sven Klemm

Takamichi Osumi

Takeshi Ideriha

Tatsuo Ishii

Ted Yu

Tels

Tender Wang

Teodor Sigaev

Thom Brown

Thomas Baehler

Thomas Krennwallner

Thomas Munro

Tim Wood

Timur Magomedov

Tobias Wendorff

Todd Cook

Tofig Aliev

Tom Lane

Tomas Vondra

Tomasz Rybak

Tomasz Szypowski

Torsten Foertsch

Toshi Harada

Tristan Partin

Triveni N

Umar Hayat

Vallimaharajan G

Vasya Boytsov

Victor Yegorov

Vignesh C

Viktor Holmberg

Vinícius Abrahão

Vinod Sridharan

Virender Singla

Vitaly Davydov

Vladlen Popolitov

Vladyslav Nebozhyn

Walid Ibrahim

Webbo Han

Wenhui Qiu

Will Mortensen

Will Storey

Wolfgang Walther

Xin Zhang

Xing Guo

Xuneng Zhou

Yan Chengpen

Yang Lei

Yaroslav Saburov

Yaroslav Syrytsia

Yasir Hussain

Yasuo Honda

Yogesh Sharma

Yonghao Lee

Yoran Heling

Yu Liang

Yugo Nagata

Yuhang Qiu

Yuki Seino

Yura Sokolov

Yurii Rashkovskii

Yushi Ogiwara

Yusuke Sugie

Yuta Katsuragi

Yuto Sasaki

Yuuki Fujii

Yuya Watari

Zane Duffield

Zeyuan Hu

Zhang Mingli

Zhihong Yu

Zhijie Hou

Zsolt Parragi
