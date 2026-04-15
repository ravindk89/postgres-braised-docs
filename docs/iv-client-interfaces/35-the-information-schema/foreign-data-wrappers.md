---
title: "35.27. foreign_data_wrappers"
id: infoschema-foreign-data-wrappers
---

## `foreign_data_wrappers`

The view `foreign_data_wrappers` contains all foreign-data wrappers defined in the current database.
Only those foreign-data wrappers are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_data_wrapper_catalog `sql_identifier`

   Name of the database that contains the foreign-data wrapper (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_data_wrapper_name `sql_identifier`

   Name of the foreign-data wrapper
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   authorization_identifier `sql_identifier`

   Name of the owner of the foreign server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   library_name `character_data`

   File name of the library that implementing this foreign-data wrapper
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   foreign_data_wrapper_language `character_data`

   Language used to implement this foreign-data wrapper
  :::{/cell}
  :::{/row}
:::{/table}

: foreign_data_wrappers Columns
