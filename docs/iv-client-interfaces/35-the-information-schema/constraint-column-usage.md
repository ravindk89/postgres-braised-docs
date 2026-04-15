---
title: "35.18. constraint_column_usage"
id: infoschema-constraint-column-usage
---

## `constraint_column_usage`

The view `constraint_column_usage` identifies all columns in the current database that are used by some constraint.
Only those columns are shown that are contained in a table owned by a currently enabled role.
For a check constraint, this view identifies the columns that are used in the check expression.
For a not-null constraint, this view identifies the column that the constraint is defined on.
For a foreign key constraint, this view identifies the columns that the foreign key references.
For a unique or primary key constraint, this view identifies the constrained columns.

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

   Name of the database that contains the table that contains the column that is used by some constraint (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that contains the column that is used by some constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that contains the column that is used by some constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column that is used by some constraint
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
:::{/table}

: constraint_column_usage Columns
