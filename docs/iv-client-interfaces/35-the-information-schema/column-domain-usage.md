---
title: "35.13. column_domain_usage"
id: infoschema-column-domain-usage
---

## `column_domain_usage`

The view `column_domain_usage` identifies all columns (of a table or a view) that make use of some domain defined in the current database and owned by a currently enabled role.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_catalog `sql_identifier`

   Name of the database containing the domain (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_schema `sql_identifier`

   Name of the schema containing the domain
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_name `sql_identifier`

   Name of the domain
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

: column_domain_usage Columns
