---
title: "35.9. check_constraints"
id: infoschema-check-constraints
---

## `check_constraints`

The view `check_constraints` contains all check constraints, either defined on a table or on a domain, that are owned by a currently enabled role. (The owner of the table or domain is the owner of the constraint.)

The SQL standard considers not-null constraints to be check constraints with a `CHECK (column_name IS NOT NULL)` expression.
So not-null constraints are also included here and don\'t have a separate view.

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

   Name of the database containing the constraint (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_schema `sql_identifier`

   Name of the schema containing the constraint
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
   check_clause `character_data`

   The check expression of the check constraint
  :::{/cell}
  :::{/row}
:::{/table}

: check_constraints Columns
