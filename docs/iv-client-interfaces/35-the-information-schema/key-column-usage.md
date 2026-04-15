---
title: "35.32. key_column_usage"
id: infoschema-key-column-usage
---

## `key_column_usage`

The view `key_column_usage` identifies all columns in the current database that are restricted by some unique, primary key, or foreign key constraint.
Check constraints are not included in this view.
Only those columns are shown that the current user has access to, by way of being the owner or having some privilege.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_catalog `sql_identifier`

   Name of the database that contains the constraint (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_schema `sql_identifier`

   Name of the schema that contains the constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_name `sql_identifier`

   Name of the constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database that contains the table that contains the column that is restricted by this constraint (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that contains the column that is restricted by this constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that contains the column that is restricted by this constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column that is restricted by this constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordinal_position `cardinal_number`

   Ordinal position of the column within the constraint key (count starts at 1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   position_in_unique_constraint `cardinal_number`

   For a foreign-key constraint, ordinal position of the referenced column within its unique constraint (count starts at 1); otherwise null
  :::{/cell}
  :::{/row}
:::{/table}

: key_column_usage Columns
