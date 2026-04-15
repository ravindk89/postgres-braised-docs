---
title: "35.31. foreign_tables"
id: infoschema-foreign-tables
---

## `foreign_tables`

The view `foreign_tables` contains all foreign tables defined in the current database.
Only those foreign tables are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_table_catalog `sql_identifier`

   Name of the database that the foreign table is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_table_schema `sql_identifier`

   Name of the schema that contains the foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_table_name `sql_identifier`

   Name of the foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_catalog `sql_identifier`

   Name of the database that the foreign server is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_name `sql_identifier`

   Name of the foreign server
  :::{/cell}
  :::{/row}
:::{/table}

: foreign_tables Columns
