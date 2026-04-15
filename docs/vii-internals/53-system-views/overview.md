---
title: "53.1. Overview"
id: views-overview
---

## Overview

System Views lists the system views.
More detailed documentation of each catalog follows below.
Except where noted, all the views described here are read-only.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  View Name
  :::{/cell}
  :::{.cell}
  Purpose
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_aios](#view-pg-aios)
  :::{/cell}
  :::{.cell}
  In-use asynchronous IO handles
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_available_extensions](#view-pg-available-extensions)
  :::{/cell}
  :::{.cell}
  available extensions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_available_extension_versions](#view-pg-available-extension-versions)
  :::{/cell}
  :::{.cell}
  available versions of extensions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_backend_memory_contexts](#view-pg-backend-memory-contexts)
  :::{/cell}
  :::{.cell}
  backend memory contexts
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_config](#view-pg-config)
  :::{/cell}
  :::{.cell}
  compile-time configuration parameters
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_cursors](#view-pg-cursors)
  :::{/cell}
  :::{.cell}
  open cursors
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_file_settings](#view-pg-file-settings)
  :::{/cell}
  :::{.cell}
  summary of configuration file contents
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_group](#view-pg-group)
  :::{/cell}
  :::{.cell}
  groups of database users
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_hba_file_rules](#view-pg-hba-file-rules)
  :::{/cell}
  :::{.cell}
  summary of client authentication configuration file contents
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ident_file_mappings](#view-pg-ident-file-mappings)
  :::{/cell}
  :::{.cell}
  summary of client user name mapping configuration file contents
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_indexes](#view-pg-indexes)
  :::{/cell}
  :::{.cell}
  indexes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_locks](#view-pg-locks)
  :::{/cell}
  :::{.cell}
  locks currently held or awaited
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_matviews](#view-pg-matviews)
  :::{/cell}
  :::{.cell}
  materialized views
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_policies](#view-pg-policies)
  :::{/cell}
  :::{.cell}
  policies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_prepared_statements](#view-pg-prepared-statements)
  :::{/cell}
  :::{.cell}
  prepared statements
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_prepared_xacts](#view-pg-prepared-xacts)
  :::{/cell}
  :::{.cell}
  prepared transactions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_publication_tables](#view-pg-publication-tables)
  :::{/cell}
  :::{.cell}
  publications and information of their associated tables
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_replication_origin_status](#view-pg-replication-origin-status)
  :::{/cell}
  :::{.cell}
  information about replication origins, including replication progress
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_replication_slots](#view-pg-replication-slots)
  :::{/cell}
  :::{.cell}
  replication slot information
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_roles](#view-pg-roles)
  :::{/cell}
  :::{.cell}
  database roles
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_rules](#view-pg-rules)
  :::{/cell}
  :::{.cell}
  rules
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_seclabels](#view-pg-seclabels)
  :::{/cell}
  :::{.cell}
  security labels
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_sequences](#view-pg-sequences)
  :::{/cell}
  :::{.cell}
  sequences
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_settings](#view-pg-settings)
  :::{/cell}
  :::{.cell}
  parameter settings
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shadow](#view-pg-shadow)
  :::{/cell}
  :::{.cell}
  database users
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shmem_allocations](#view-pg-shmem-allocations)
  :::{/cell}
  :::{.cell}
  shared memory allocations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shmem_allocations_numa](#view-pg-shmem-allocations-numa)
  :::{/cell}
  :::{.cell}
  NUMA node mappings for shared memory allocations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_stats](#view-pg-stats)
  :::{/cell}
  :::{.cell}
  planner statistics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_stats_ext](#view-pg-stats-ext)
  :::{/cell}
  :::{.cell}
  extended planner statistics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_stats_ext_exprs](#view-pg-stats-ext-exprs)
  :::{/cell}
  :::{.cell}
  extended planner statistics for expressions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_tables](#view-pg-tables)
  :::{/cell}
  :::{.cell}
  tables
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_timezone_abbrevs](#view-pg-timezone-abbrevs)
  :::{/cell}
  :::{.cell}
  time zone abbreviations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_timezone_names](#view-pg-timezone-names)
  :::{/cell}
  :::{.cell}
  time zone names
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_user](#view-pg-user)
  :::{/cell}
  :::{.cell}
  database users
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_user_mappings](#view-pg-user-mappings)
  :::{/cell}
  :::{.cell}
  user mappings
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_views](#view-pg-views)
  :::{/cell}
  :::{.cell}
  views
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_wait_events](#view-pg-wait-events)
  :::{/cell}
  :::{.cell}
  wait events
  :::{/cell}
  :::{/row}
:::{/table}

  : System Views
