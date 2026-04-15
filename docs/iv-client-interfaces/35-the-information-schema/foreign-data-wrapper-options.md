---
title: "35.26. foreign_data_wrapper_options"
id: infoschema-foreign-data-wrapper-options
---

## `foreign_data_wrapper_options`

The view `foreign_data_wrapper_options` contains all the options defined for foreign-data wrappers in the current database.
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

   Name of the database that the foreign-data wrapper is defined in (always the current database)
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

: foreign_data_wrapper_options Columns
