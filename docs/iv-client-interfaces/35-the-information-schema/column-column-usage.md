---
title: "35.12. column_column_usage"
id: infoschema-column-column-usage
---

## `column_column_usage`

The view `column_column_usage` identifies all generated columns that depend on another base column in the same table.
Only tables owned by a currently enabled role are included.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database containing the table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema containing the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the base column that a generated column depends on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dependent_column `sql_identifier`

   Name of the generated column
  :::{/cell}
  :::{/row}
:::{/table}

: column_column_usage Columns
