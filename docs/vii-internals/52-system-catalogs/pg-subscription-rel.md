---
title: "52.55. pg_subscription_rel"
id: catalog-pg-subscription-rel
---

## pg_subscription_rel

The catalog pg_subscription_rel contains the state for each replicated relation in each subscription.
This is a many-to-many mapping.

This catalog only contains tables known to the subscription after running either [`CREATE SUBSCRIPTION`](#sql-createsubscription) or [`ALTER SUBSCRIPTION ... REFRESH PUBLICATION`](#sql-altersubscription).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srsubid `oid` (references [pg_subscription](#catalog-pg-subscription).oid)

   Reference to subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   Reference to relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srsubstate `char`

   State code: `i` = initialize, `d` = data is being copied, `f` = finished table copy, `s` = synchronized, `r` = ready (normal replication)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srsublsn `pg_lsn`

   Remote LSN of the state change used for synchronization coordination when in `s` or `r` states, otherwise null
  :::{/cell}
  :::{/row}
:::{/table}

: pg_subscription_rel Columns
