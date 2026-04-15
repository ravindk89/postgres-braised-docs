---
title: "35.60. user_defined_types"
id: infoschema-user-defined-types
---

## `user_defined_types`

The view `user_defined_types` currently contains all composite types defined in the current database.
Only those types are shown that the current user has access to (by way of being the owner or having some privilege).

SQL knows about two kinds of user-defined types: structured types (also known as composite types in PostgreSQL) and distinct types (not implemented in PostgreSQL).
To be future-proof, use the column `user_defined_type_category` to differentiate between these.
Other user-defined types such as base types and enums, which are PostgreSQL extensions, are not shown here.
For domains, see [domains](braised:ref/infoschema-domains) instead.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_catalog `sql_identifier`

   Name of the database that contains the type (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_schema `sql_identifier`

   Name of the schema that contains the type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_name `sql_identifier`

   Name of the type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_defined_type_category `character_data`

   Currently always `STRUCTURED`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_instantiable `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_final `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordering_form `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordering_category `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordering_routine_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordering_routine_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ordering_routine_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reference_type `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   data_type `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_maximum_length `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_octet_length `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_set_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_set_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_set_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision_radix `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_scale `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datetime_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_type `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   source_dtd_identifier `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ref_dtd_identifier `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
:::{/table}

: user_defined_types Columns
