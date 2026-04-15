---
title: "35.50. sql_parts"
id: infoschema-sql-parts
---

## `sql_parts`

The table `sql_parts` contains information about which of the several parts of the SQL standard are supported by PostgreSQL.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   feature_id `character_data`

   An identifier string containing the number of the part
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   feature_name `character_data`

   Descriptive name of the part
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_supported `yes_or_no`

   `YES` if the part is fully supported by the current version of PostgreSQL, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_verified_by `character_data`

   Always null, since the PostgreSQL development group does not perform formal testing of feature conformance
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   comments `character_data`

   Possibly a comment about the supported status of the part
  :::{/cell}
  :::{/row}
:::{/table}

: sql_parts Columns
