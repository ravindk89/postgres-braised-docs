---
title: "35.62. user_mappings"
id: infoschema-user-mappings
---

## `user_mappings`

The view `user_mappings` contains all user mappings defined in the current database.
Only those user mappings are shown where the current user has access to the corresponding foreign server (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   authorization_identifier `sql_identifier`

   Name of the user being mapped, or `PUBLIC` if the mapping is public
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_catalog `sql_identifier`

   Name of the database that the foreign server used by this mapping is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_server_name `sql_identifier`

   Name of the foreign server used by this mapping
  :::{/cell}
  :::{/row}
:::{/table}

: user_mappings Columns
