---
title: "35.52. table_constraints"
id: infoschema-table-constraints
---

## `table_constraints`

The view `table_constraints` contains all constraints belonging to tables that the current user owns or has some privilege other than `SELECT` on.

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

   Name of the database that contains the table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table
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
   constraint_type `character_data`

   Type of the constraint: `CHECK` (includes not-null constraints), `FOREIGN KEY`, `PRIMARY KEY`, or `UNIQUE`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_deferrable `yes_or_no`

   `YES` if the constraint is deferrable, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   initially_deferred `yes_or_no`

   `YES` if the constraint is deferrable and initially deferred, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   enforced `yes_or_no`

   `YES` if the constraint is enforced, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   nulls_distinct `yes_or_no`

   If the constraint is a unique constraint, then `YES` if the constraint treats nulls as distinct or `NO` if it treats nulls as not distinct, otherwise null for other types of constraints.
  :::{/cell}
  :::{/row}
:::{/table}

: table_constraints Columns
