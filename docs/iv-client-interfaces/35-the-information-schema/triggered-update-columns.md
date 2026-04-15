---
title: "35.56. triggered_update_columns"
id: infoschema-triggered-update-columns
---

## `triggered_update_columns`

For triggers in the current database that specify a column list (like `UPDATE OF column1, column2`), the view `triggered_update_columns` identifies these columns.
Triggers that do not specify a column list are not included in this view.
Only those columns are shown that the current user owns or has some privilege other than `SELECT` on.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trigger_catalog `sql_identifier`

   Name of the database that contains the trigger (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trigger_schema `sql_identifier`

   Name of the schema that contains the trigger
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trigger_name `sql_identifier`

   Name of the trigger
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   event_object_catalog `sql_identifier`

   Name of the database that contains the table that the trigger is defined on (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   event_object_schema `sql_identifier`

   Name of the schema that contains the table that the trigger is defined on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   event_object_table `sql_identifier`

   Name of the table that the trigger is defined on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   event_object_column `sql_identifier`

   Name of the column that the trigger is defined on
  :::{/cell}
  :::{/row}
:::{/table}

: triggered_update_columns Columns
