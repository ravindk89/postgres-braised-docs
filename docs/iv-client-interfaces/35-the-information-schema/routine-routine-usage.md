---
title: "35.42. routine_routine_usage"
id: infoschema-routine-routine-usage
---

## `routine_routine_usage`

The view `routine_routine_usage` identifies all functions or procedures that are used by another (or the same) function or procedure, either in the SQL body or in parameter default expressions. (This only works for unquoted SQL bodies, not quoted bodies or functions in other languages.) An entry is included here only if the used function is owned by a currently enabled role. (There is no such restriction on the using function.)

Note that the entries for both functions in the view refer to the "specific" name of the routine, even though the column names are used in a way that is inconsistent with other information schema views about routines.
This is per SQL standard, although it is arguably a misdesign.
See [routines](braised:ref/infoschema-routines) for more information about specific names.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_catalog `sql_identifier`

   Name of the database containing the using function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_schema `sql_identifier`

   Name of the schema containing the using function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_name `sql_identifier`

   The "specific name" of the using function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_catalog `sql_identifier`

   Name of the database that contains the function that is used by the first function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_schema `sql_identifier`

   Name of the schema that contains the function that is used by the first function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_name `sql_identifier`

   The "specific name" of the function that is used by the first function.
  :::{/cell}
  :::{/row}
:::{/table}

: `routine_routine_usage` Columns
