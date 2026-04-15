---
title: "35.46. schemata"
id: infoschema-schemata
---

## `schemata`

The view `schemata` contains all schemas in the current database that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   catalog_name `sql_identifier`

   Name of the database that the schema is contained in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schema_name `sql_identifier`

   Name of the schema
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schema_owner `sql_identifier`

   Name of the owner of the schema
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   default_character_set_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   default_character_set_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   default_character_set_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sql_path `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
:::{/table}

: schemata Columns
