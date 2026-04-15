---
title: "53.16. pg_prepared_statements"
id: view-pg-prepared-statements
---

## pg_prepared_statements

The pg_prepared_statements view displays all the prepared statements that are available in the current session.
See [PREPARE](braised:ref/sql-prepare) for more information about prepared statements.

pg_prepared_statements contains one row for each prepared statement.
Rows are added to the view when a new prepared statement is created and removed when a prepared statement is released (for example, via the [`DEALLOCATE`](#sql-deallocate) command).

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

   The identifier of the prepared statement
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   statement `text`

   The query string submitted by the client to create this prepared statement. For prepared statements created via SQL, this is the `PREPARE` statement submitted by the client. For prepared statements created via the frontend/backend protocol, this is the text of the prepared statement itself.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prepare_time `timestamptz`

   The time at which the prepared statement was created
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parameter_types `regtype[]`

   The expected parameter types for the prepared statement in the form of an array of `regtype`. The OID corresponding to an element of this array can be obtained by casting the `regtype` value to `oid`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_types `regtype[]`

   The types of the columns returned by the prepared statement in the form of an array of `regtype`. The OID corresponding to an element of this array can be obtained by casting the `regtype` value to `oid`. If the prepared statement does not provide a result (e.g., a DML statement), then this field will be null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   from_sql `bool`

   `true` if the prepared statement was created via the `PREPARE` SQL command; `false` if the statement was prepared via the frontend/backend protocol
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   generic_plans `int8`

   Number of times generic plan was chosen
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   custom_plans `int8`

   Number of times custom plan was chosen
  :::{/cell}
  :::{/row}
:::{/table}

: pg_prepared_statements Columns

The pg_prepared_statements view is read-only.
