---
title: "35.51. sql_sizing"
id: infoschema-sql-sizing
---

## `sql_sizing`

The table `sql_sizing` contains information about various size limits and maximum values in PostgreSQL.
This information is primarily intended for use in the context of the ODBC interface; users of other interfaces will probably find this information to be of little use.
For this reason, the individual sizing items are not described here; you will find them in the description of the ODBC interface.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sizing_id `cardinal_number`

   Identifier of the sizing item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sizing_name `character_data`

   Descriptive name of the sizing item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   supported_value `cardinal_number`

   Value of the sizing item, or 0 if the size is unlimited or cannot be determined, or null if the features for which the sizing item is applicable are not supported
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   comments `character_data`

   Possibly a comment pertaining to the sizing item
  :::{/cell}
  :::{/row}
:::{/table}

: sql_sizing Columns
