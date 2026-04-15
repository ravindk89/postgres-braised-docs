---
title: "53.19. pg_replication_origin_status"
id: view-pg-replication-origin-status
---

## pg_replication_origin_status

The pg_replication_origin_status view contains information about how far replay for a certain origin has progressed.
For more on replication origins see [Replication Progress Tracking](braised:ref/replication-origins).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   local_id `oid` (references [pg_replication_origin](#catalog-pg-replication-origin).roident)

   internal node identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   external_id `text` (references [pg_replication_origin](#catalog-pg-replication-origin).roname)

   external node identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   remote_lsn `pg_lsn`

   The origin node\'s LSN up to which data has been replicated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   local_lsn `pg_lsn`

   This node\'s LSN at which `remote_lsn` has been replicated. Used to flush commit records before persisting data to disk when using asynchronous commits.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_replication_origin_status Columns
