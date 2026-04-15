---
title: "35.41. routine_privileges"
id: infoschema-routine-privileges
---

## `routine_privileges`

The view `routine_privileges` identifies all privileges granted on functions to a currently enabled role or by a currently enabled role.
There is one row for each combination of function, grantor, and grantee.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantor `sql_identifier`

   Name of the role that granted the privilege
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantee `sql_identifier`

   Name of the role that the privilege was granted to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_catalog `sql_identifier`

   Name of the database containing the function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_schema `sql_identifier`

   Name of the schema containing the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_name `sql_identifier`

   The "specific name" of the function. See [routines](braised:ref/infoschema-routines) for more information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_catalog `sql_identifier`

   Name of the database containing the function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_schema `sql_identifier`

   Name of the schema containing the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_name `sql_identifier`

   Name of the function (might be duplicated in case of overloading)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privilege_type `character_data`

   Always `EXECUTE` (the only privilege type for functions)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   `YES` if the privilege is grantable, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: routine_privileges Columns
