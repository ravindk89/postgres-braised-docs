---
title: "35.49. sql_implementation_info"
id: infoschema-sql-implementation-info
---

## `sql_implementation_info`

The table `sql_implementation_info` contains information about various aspects that are left implementation-defined by the SQL standard.
This information is primarily intended for use in the context of the ODBC interface; users of other interfaces will probably find this information to be of little use.
For this reason, the individual implementation information items are not described here; you will find them in the description of the ODBC interface.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   implementation_info_id `character_data`

   Identifier string of the implementation information item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   implementation_info_name `character_data`

   Descriptive name of the implementation information item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   integer_value `cardinal_number`

   Value of the implementation information item, or null if the value is contained in the column `character_value`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_value `character_data`

   Value of the implementation information item, or null if the value is contained in the column `integer_value`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   comments `character_data`

   Possibly a comment pertaining to the implementation information item
  :::{/cell}
  :::{/row}
:::{/table}

: sql_implementation_info Columns
