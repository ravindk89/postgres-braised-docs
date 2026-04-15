---
title: "35.11. collation_character_set_​applicability"
id: infoschema-collation-character-set-applicab
---

## `collation_character_set_​applicability`

The view `collation_character_set_applicability` identifies which character set the available collations are applicable to.
In PostgreSQL, there is only one character set per database (see explanation in [character_sets](braised:ref/infoschema-character-sets)), so this view does not provide much useful information.

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
   character_set_catalog `sql_identifier`

   Character sets are currently not implemented as schema objects, so this column is null
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_set_schema `sql_identifier`

   Character sets are currently not implemented as schema objects, so this column is null
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_set_name `sql_identifier`

   Name of the character set
  :::{/cell}
  :::{/row}
:::{/table}

: collation_character_set_applicability Columns
