---
title: "35.16. column_udt_usage"
id: infoschema-column-udt-usage
---

## `column_udt_usage`

The view `column_udt_usage` identifies all columns that use data types owned by a currently enabled role.
Note that in PostgreSQL, built-in data types behave like user-defined types, so they are included here as well.
See also [columns](braised:ref/infoschema-columns) for details.

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

   Name of the database that the column data type (the underlying type of the domain, if applicable) is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Name of the schema that the column data type (the underlying type of the domain, if applicable) is defined in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Name of the column data type (the underlying type of the domain, if applicable)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database containing the table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema containing the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column
  :::{/cell}
  :::{/row}
:::{/table}

: column_udt_usage Columns
