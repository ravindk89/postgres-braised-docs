---
title: "35.54. tables"
id: infoschema-tables
---

## `tables`

The view `tables` contains all tables and views defined in the current database.
Only those tables and views are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database that contains the table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table
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
   table_type `character_data`

   Type of the table: `BASE TABLE` for a persistent base table (the normal table type), `VIEW` for a view, `FOREIGN` for a foreign table, or `LOCAL TEMPORARY` for a temporary table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   self_referencing_column_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reference_generation `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_catalog `sql_identifier`

   If the table is a typed table, the name of the database that contains the underlying data type (always the current database), else null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_schema `sql_identifier`

   If the table is a typed table, the name of the schema that contains the underlying data type, else null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_name `sql_identifier`

   If the table is a typed table, the name of the underlying data type, else null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_insertable_into `yes_or_no`

   `YES` if the table is insertable into, `NO` if not (Base tables are always insertable into, views not necessarily.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_typed `yes_or_no`

   `YES` if the table is a typed table, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   commit_action `character_data`

   Not yet implemented
  :::{/cell}
  :::{/row}
:::{/table}

: tables Columns
