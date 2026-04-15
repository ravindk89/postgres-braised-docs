---
title: "35.65. view_table_usage"
id: infoschema-view-table-usage
---

## `view_table_usage`

The view `view_table_usage` identifies all tables that are used in the query expression of a view (the `SELECT` statement that defines the view).
A table is only included if that table is owned by a currently enabled role.

:::{.callout type="note"}
System tables are not included. This should be fixed sometime.
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

   Name of the database that contains the table that is used by the view (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that is used by the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that is used by the view
  :::{/cell}
  :::{/row}
:::{/table}

: view_table_usage Columns
