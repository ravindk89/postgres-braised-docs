---
title: "35.28. foreign_server_options"
id: infoschema-foreign-server-options
---

## `foreign_server_options`

The view `foreign_server_options` contains all the options defined for foreign servers in the current database.
Only those foreign servers are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
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

: foreign_server_options Columns
