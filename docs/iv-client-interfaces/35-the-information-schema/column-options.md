---
title: "35.14. column_options"
id: infoschema-column-options
---

## `column_options`

The view `column_options` contains all the options defined for foreign table columns in the current database.
Only those foreign table columns are shown that the current user has access to (by way of being the owner or having some privilege).

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

   Name of the database that contains the foreign table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column
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

: column_options Columns
