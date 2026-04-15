---
title: "53.24. pg_sequences"
id: view-pg-sequences
---

## pg_sequences

The view pg_sequences provides access to useful information about each sequence in the database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name` (references [pg_namespace](#catalog-pg-namespace).nspname)

   Name of schema containing sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sequencename `name` (references [pg_class](#catalog-pg-class).relname)

   Name of sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sequenceowner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of sequence\'s owner
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   data_type `regtype` (references [pg_type](#catalog-pg-type).oid)

   Data type of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   start_value `int8`

   Start value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   min_value `int8`

   Minimum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   max_value `int8`

   Maximum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   increment_by `int8`

   Increment value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cycle `bool`

   Whether the sequence cycles
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cache_size `int8`

   Cache size of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_value `int8`

   The last sequence value written to disk. If caching is used, this value can be greater than the last value handed out from the sequence.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_sequences Columns

The last_value column will read as null if any of the following are true:

-   The sequence has not been read from yet.

-   The current user does not have `USAGE` or `SELECT` privilege on the sequence.

-   The sequence is unlogged and the server is a standby.
