---
title: "35.10. collations"
id: infoschema-collations
---

## `collations`

The view `collations` contains the collations available in the current database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_catalog `sql_identifier`

   Name of the database containing the collation (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_schema `sql_identifier`

   Name of the schema containing the collation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_name `sql_identifier`

   Name of the default collation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pad_attribute `character_data`

   Always `NO PAD` (The alternative `PAD SPACE` is not supported by PostgreSQL.)
  :::{/cell}
  :::{/row}
:::{/table}

: collations Columns
