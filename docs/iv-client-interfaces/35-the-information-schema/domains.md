---
title: "35.23. domains"
id: infoschema-domains
---

## `domains`

The view `domains` contains all domains defined in the current database.
Only those domains are shown that the current user has access to (by way of being the owner or having some privilege).

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
  :::{.row}
  :::{.cell}
   data_type `character_data`

   Data type of the domain, if it is a built-in type, or `ARRAY` if it is some array (in that case, see the view `element_types`), else `USER-DEFINED` (in that case, the type is identified in `udt_name` and associated columns).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_maximum_length `cardinal_number`

   If the domain has a character or bit string type, the declared maximum length; null for all other data types or if no maximum length was declared.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   character_octet_length `cardinal_number`

   If the domain has a character type, the maximum possible length in octets (bytes) of a datum; null for all other data types. The maximum octet length depends on the declared character maximum length (see above) and the server encoding.
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

   Name of the database containing the collation of the domain (always the current database), null if default or the data type of the domain is not collatable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_schema `sql_identifier`

   Name of the schema containing the collation of the domain, null if default or the data type of the domain is not collatable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collation_name `sql_identifier`

   Name of the collation of the domain, null if default or the data type of the domain is not collatable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision `cardinal_number`

   If the domain has a numeric type, this column contains the (declared or implicit) precision of the type for this domain. The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column `numeric_precision_radix`. For all other data types, this column is null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision_radix `cardinal_number`

   If the domain has a numeric type, this column indicates in which base the values in the columns `numeric_precision` and `numeric_scale` are expressed. The value is either 2 or 10. For all other data types, this column is null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_scale `cardinal_number`

   If the domain has an exact numeric type, this column contains the (declared or implicit) scale of the type for this domain. The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column `numeric_precision_radix`. For all other data types, this column is null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datetime_precision `cardinal_number`

   If `data_type` identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this domain, that is, the number of decimal digits maintained following the decimal point in the seconds value. For all other data types, this column is null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_type `character_data`

   If `data_type` identifies an interval type, this column contains the specification which fields the intervals include for this domain, e.g., `YEAR TO MONTH`, `DAY TO SECOND`, etc. If no field restrictions were specified (that is, the interval accepts all fields), and for all other data types, this field is null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   interval_precision `cardinal_number`

   Applies to a feature not available in PostgreSQL (see `datetime_precision` for the fractional seconds precision of interval type domains)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_default `character_data`

   Default expression of the domain
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

   An identifier of the data type descriptor of the domain, unique among the data type descriptors pertaining to the domain (which is trivial, because a domain only contains one data type descriptor). This is mainly useful for joining with other instances of such identifiers. (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)
  :::{/cell}
  :::{/row}
:::{/table}

: domains Columns
