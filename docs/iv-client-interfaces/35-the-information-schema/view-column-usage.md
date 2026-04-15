---
title: "35.63. view_column_usage"
id: infoschema-view-column-usage
---

## `view_column_usage`

The view `view_column_usage` identifies all columns that are used in the query expression of a view (the `SELECT` statement that defines the view).
A column is only included if the table that contains the column is owned by a currently enabled role.

:::{.callout type="note"}
Columns of system tables are not included. This should be fixed sometime.
:::

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   view_catalog `sql_identifier`

   Name of the database that contains the view (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   view_schema `sql_identifier`

   Name of the schema that contains the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   view_name `sql_identifier`

   Name of the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database that contains the table that contains the column that is used by the view (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that contains the column that is used by the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that contains the column that is used by the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column that is used by the view
  :::{/cell}
  :::{/row}
:::{/table}

: view_column_usage Columns
