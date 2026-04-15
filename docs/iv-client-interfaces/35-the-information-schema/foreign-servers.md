---
title: "35.29. foreign_servers"
id: infoschema-foreign-servers
---

## `foreign_servers`

The view `foreign_servers` contains all foreign servers defined in the current database.
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
   foreign_data_wrapper_catalog `sql_identifier`

   Name of the database that contains the foreign-data wrapper used by the foreign server (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_data_wrapper_name `sql_identifier`

   Name of the foreign-data wrapper used by the foreign server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_type `character_data`

   Foreign server type information, if specified upon creation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_version `character_data`

   Foreign server version information, if specified upon creation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   authorization_identifier `sql_identifier`

   Name of the owner of the foreign server
  :::{/cell}
  :::{/row}
:::{/table}

: foreign_servers Columns
