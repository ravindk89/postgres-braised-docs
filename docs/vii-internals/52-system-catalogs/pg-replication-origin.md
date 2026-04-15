---
title: "52.44. pg_replication_origin"
id: catalog-pg-replication-origin
---

## pg_replication_origin

The pg_replication_origin catalog contains all replication origins created.
For more on replication origins see [Replication Progress Tracking](braised:ref/replication-origins).

Unlike most system catalogs, pg_replication_origin is shared across all databases of a cluster: there is only one copy of pg_replication_origin per cluster, not one per database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   roident `oid`

   A unique, cluster-wide identifier for the replication origin. Should never leave the system.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   roname `text`

   The external, user defined, name of a replication origin.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_replication_origin Columns
