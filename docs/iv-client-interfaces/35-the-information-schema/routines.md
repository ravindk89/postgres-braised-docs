---
title: "35.45. routines"
id: infoschema-routines
---

## `routines`

The view `routines` contains all functions and procedures in the current database.
Only those functions and procedures are shown that the current user has access to (by way of being the owner or having some privilege).

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

   The "specific name" of the function. This is a name that uniquely identifies the function in the schema, even if the real name of the function is overloaded. The format of the specific name is not defined, it should only be used to compare it to other instances of specific routine names.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_catalog `sql_identifier`

   Name of the database containing the function (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_schema `sql_identifier`

   Name of the schema containing the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_name `sql_identifier`

   Name of the function (might be duplicated in case of overloading)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_type `character_data`

   `FUNCTION` for a function, `PROCEDURE` for a procedure
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   module_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   module_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   module_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   data_type `character_data`

   Return data type of the function, if it is a built-in type, or `ARRAY` if it is some array (in that case, see the view `element_types`), else `USER-DEFINED` (in that case, the type is identified in `type_udt_name` and associated columns). Null for a procedure.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_maximum_length `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_octet_length `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
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

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_schema `sql_identifier`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_name `sql_identifier`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision_radix `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_scale `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datetime_precision `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_type `character_data`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_precision `cardinal_number`

   Always null, since this information is not applied to return data types in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   type_udt_catalog `sql_identifier`

   Name of the database that the return data type of the function is defined in (always the current database). Null for a procedure.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   type_udt_schema `sql_identifier`

   Name of the schema that the return data type of the function is defined in. Null for a procedure.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   type_udt_name `sql_identifier`

   Name of the return data type of the function. Null for a procedure.
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

   An identifier of the data type descriptor of the return data type of this function, unique among the data type descriptors pertaining to the function. This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_body `character_data`

   If the function is an SQL function, then `SQL`, else `EXTERNAL`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   routine_definition `character_data`

   The source text of the function (null if the function is not owned by a currently enabled role). (According to the SQL standard, this column is only applicable if `routine_body` is `SQL`, but in PostgreSQL it will contain whatever source text was specified when the function was created.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   external_name `character_data`

   If this function is a C function, then the external name (link symbol) of the function; else null. (This works out to be the same value that is shown in `routine_definition`.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   external_language `character_data`

   The language the function is written in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   parameter_style `character_data`

   Always `GENERAL` (The SQL standard defines other parameter styles, which are not available in PostgreSQL.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_deterministic `yes_or_no`

   If the function is declared immutable (called deterministic in the SQL standard), then `YES`, else `NO`. (You cannot query the other volatility levels available in PostgreSQL through the information schema.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sql_data_access `character_data`

   Always `MODIFIES`, meaning that the function possibly modifies SQL data. This information is not useful for PostgreSQL.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_null_call `yes_or_no`

   If the function automatically returns null if any of its arguments are null, then `YES`, else `NO`. Null for a procedure.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sql_path `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schema_level_routine `yes_or_no`

   Always `YES` (The opposite would be a method of a user-defined type, which is a feature not available in PostgreSQL.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   max_dynamic_result_sets `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_user_defined_cast `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_implicitly_invocable `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   security_type `character_data`

   If the function runs with the privileges of the current user, then `INVOKER`, if the function runs with the privileges of the user who defined it, then `DEFINER`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   to_sql_specific_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   to_sql_specific_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   to_sql_specific_name `sql_identifier`

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
   created `time_stamp`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   last_altered `time_stamp`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   new_savepoint_level `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_udt_dependent `yes_or_no`

   Currently always `NO`. The alternative `YES` applies to a feature not available in PostgreSQL.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_from_data_type `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_as_locator `yes_or_no`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_char_max_length `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_char_octet_length `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_char_set_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_char_set_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_char_set_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_collation_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_collation_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_collation_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_numeric_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_numeric_precision_radix `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_numeric_scale `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_datetime_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_interval_type `character_data`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_interval_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_type_udt_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_type_udt_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_type_udt_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_scope_catalog `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_scope_schema `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_scope_name `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_maximum_cardinality `cardinal_number`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result_cast_dtd_identifier `sql_identifier`

   Applies to a feature not available in PostgreSQL
  :::{/cell}
  :::{/row}
:::{/table}

: routines Columns
