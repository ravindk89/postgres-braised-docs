---
title: "35.22. domain_udt_usage"
id: infoschema-domain-udt-usage
---

## `domain_udt_usage`

The view `domain_udt_usage` identifies all domains that are based on data types owned by a currently enabled role.
Note that in PostgreSQL, built-in data types behave like user-defined types, so they are included here as well.

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

   Name of the database that the domain data type is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Name of the schema that the domain data type is defined in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Name of the domain data type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_catalog `sql_identifier`

   Name of the database that contains the domain (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_schema `sql_identifier`

   Name of the schema that contains the domain
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_name `sql_identifier`

   Name of the domain
  :::{/cell}
  :::{/row}
:::{/table}

: domain_udt_usage Columns
