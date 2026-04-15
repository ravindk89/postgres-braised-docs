---
title: "35.33. parameters"
id: infoschema-parameters
---

## `parameters`

The view `parameters` contains information about the parameters (arguments) of all functions in the current database.
Only those functions are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
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
   ordinal_position `cardinal_number`

   Ordinal position of the parameter in the argument list of the function (count starts at 1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parameter_mode `character_data`

   `IN` for input parameter, `OUT` for output parameter, and `INOUT` for input/output parameter.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_result `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   as_locator `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parameter_name `sql_identifier`

   Name of the parameter, or null if the parameter has no name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   data_type `character_data`

   Data type of the parameter, if it is a built-in type, or `ARRAY` if it is some array (in that case, see the view `element_types`), else `USER-DEFINED` (in that case, the type is identified in `udt_name` and associated columns).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_maximum_length `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_octet_length `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
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

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_schema `sql_identifier`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_name `sql_identifier`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision_radix `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_scale `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datetime_precision `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_type `character_data`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_precision `cardinal_number`

   Always null, since this information is not applied to parameter data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_catalog `sql_identifier`

   Name of the database that the data type of the parameter is defined in (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Name of the schema that the data type of the parameter is defined in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Name of the data type of the parameter
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   scope_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   scope_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   scope_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   maximum_cardinality `cardinal_number`

   Always null, because arrays always have unlimited maximum cardinality in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dtd_identifier `sql_identifier`

   An identifier of the data type descriptor of the parameter, unique among the data type descriptors pertaining to the function. This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parameter_default `character_data`

   The default expression of the parameter, or null if none or if the function is not owned by a currently enabled role.
  :::{/cell}
  :::{/row}
:::{/table}

: parameters Columns
