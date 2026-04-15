---
title: "35.55. transforms"
id: infoschema-transforms
---

## `transforms`

The view `transforms` contains information about the transforms defined in the current database.
More precisely, it contains a row for each function contained in a transform (the "from SQL" or "to SQL" function).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_catalog `sql_identifier`

   Name of the database that contains the type the transform is for (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Name of the schema that contains the type the transform is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Name of the type the transform is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_catalog `sql_identifier`

   Name of the database containing the function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_schema `sql_identifier`

   Name of the schema containing the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   specific_name `sql_identifier`

   The "specific name" of the function. See [routines](braised:ref/infoschema-routines) for more information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   group_name `sql_identifier`

   The SQL standard allows defining transforms in "groups", and selecting a group at run time. PostgreSQL does not support this. Instead, transforms are specific to a language. As a compromise, this field contains the language the transform is for.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   transform_type `character_data`

   `FROM SQL` or `TO SQL`
  :::{/cell}
  :::{/row}
:::{/table}

: transforms Columns
