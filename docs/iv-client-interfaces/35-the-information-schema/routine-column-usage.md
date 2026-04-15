---
title: "35.40. routine_column_usage"
id: infoschema-routine-column-usage
---

## `routine_column_usage`

The view `routine_column_usage` identifies all columns that are used by a function or procedure, either in the SQL body or in parameter default expressions. (This only works for unquoted SQL bodies, not quoted bodies or functions in other languages.) A column is only included if its table is owned by a currently enabled role.

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
   table_catalog `sql_identifier`

   Name of the database that contains the table that is used by the function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that is used by the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that is used by the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column that is used by the function
  :::{/cell}
  :::{/row}
:::{/table}

: `routine_column_usage` Columns
