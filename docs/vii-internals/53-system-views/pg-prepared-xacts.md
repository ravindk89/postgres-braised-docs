---
title: "53.17. pg_prepared_xacts"
id: view-pg-prepared-xacts
---

## pg_prepared_xacts

The view pg_prepared_xacts displays information about transactions that are currently prepared for two-phase commit (see [PREPARE TRANSACTION](braised:ref/sql-prepare-transaction) for details).

pg_prepared_xacts contains one row per prepared transaction.
An entry is removed when the transaction is committed or rolled back.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   transaction `xid`

   Numeric transaction identifier of the prepared transaction
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   gid `text`

   Global transaction identifier that was assigned to the transaction
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prepared `timestamptz`

   Time at which the transaction was prepared for commit
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   owner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of the user that executed the transaction
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   database `name` (references [pg_database](#catalog-pg-database).datname)

   Name of the database in which the transaction was executed
  :::{/cell}
  :::{/row}
:::{/table}

: pg_prepared_xacts Columns

When the pg_prepared_xacts view is accessed, the internal transaction manager data structures are momentarily locked, and a copy is made for the view to display. This ensures that the view produces a consistent set of results, while not blocking normal operations longer than necessary. Nonetheless there could be some impact on database performance if this view is frequently accessed.
