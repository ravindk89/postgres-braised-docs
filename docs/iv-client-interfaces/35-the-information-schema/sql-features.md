---
title: "35.48. sql_features"
id: infoschema-sql-features
---

## `sql_features`

The table `sql_features` contains information about which formal features defined in the SQL standard are supported by PostgreSQL.
This is the same information that is presented in [SQL Conformance](#sql-conformance).
There you can also find some additional background information.

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

   Identifier string of the feature
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   feature_name `character_data`

   Descriptive name of the feature
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sub_feature_id `character_data`

   Identifier string of the subfeature, or a zero-length string if not a subfeature
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sub_feature_name `character_data`

   Descriptive name of the subfeature, or a zero-length string if not a subfeature
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_supported `yes_or_no`

   `YES` if the feature is fully supported by the current version of PostgreSQL, `NO` if not
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

   Possibly a comment about the supported status of the feature
  :::{/cell}
  :::{/row}
:::{/table}

: sql_features Columns
