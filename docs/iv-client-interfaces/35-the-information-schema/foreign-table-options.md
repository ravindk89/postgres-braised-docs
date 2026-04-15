---
title: "35.30. foreign_table_options"
id: infoschema-foreign-table-options
---

## `foreign_table_options`

The view `foreign_table_options` contains all the options defined for foreign tables in the current database.
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

   Name of the database that contains the foreign table (always the current database)
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
   option_name `sql_identifier`

   Name of an option
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   option_value `character_data`

   Value of the option
  :::{/cell}
  :::{/row}
:::{/table}

: foreign_table_options Columns
