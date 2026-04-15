---
title: "35.34. referential_constraints"
id: infoschema-referential-constraints
---

## `referential_constraints`

The view `referential_constraints` contains all referential (foreign key) constraints in the current database.
Only those constraints are shown for which the current user has write access to the referencing table (by way of being the owner or having some privilege other than `SELECT`).

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
   unique_constraint_catalog `sql_identifier`

   Name of the database that contains the unique or primary key constraint that the foreign key constraint references (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   unique_constraint_schema `sql_identifier`

   Name of the schema that contains the unique or primary key constraint that the foreign key constraint references
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   unique_constraint_name `sql_identifier`

   Name of the unique or primary key constraint that the foreign key constraint references
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   match_option `character_data`

   Match option of the foreign key constraint: `FULL`, `PARTIAL`, or `NONE`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   update_rule `character_data`

   Update rule of the foreign key constraint: `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, or `NO ACTION`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   delete_rule `character_data`

   Delete rule of the foreign key constraint: `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, or `NO ACTION`.
  :::{/cell}
  :::{/row}
:::{/table}

: referential_constraints Columns
