---
title: "35.47. sequences"
id: infoschema-sequences
---

## `sequences`

The view `sequences` contains all sequences defined in the current database.
Only those sequences are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sequence_catalog `sql_identifier`

   Name of the database that contains the sequence (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sequence_schema `sql_identifier`

   Name of the schema that contains the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sequence_name `sql_identifier`

   Name of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   data_type `character_data`

   The data type of the sequence.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision `cardinal_number`

   This column contains the (declared or implicit) precision of the sequence data type (see above). The precision indicates the number of significant digits. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column `numeric_precision_radix`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_precision_radix `cardinal_number`

   This column indicates in which base the values in the columns `numeric_precision` and `numeric_scale` are expressed. The value is either 2 or 10.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   numeric_scale `cardinal_number`

   This column contains the (declared or implicit) scale of the sequence data type (see above). The scale indicates the number of significant digits to the right of the decimal point. It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column `numeric_precision_radix`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   start_value `character_data`

   The start value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   minimum_value `character_data`

   The minimum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   maximum_value `character_data`

   The maximum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   increment `character_data`

   The increment of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cycle_option `yes_or_no`

   `YES` if the sequence cycles, else `NO`
  :::{/cell}
  :::{/row}
:::{/table}

: sequences Columns

Note that in accordance with the SQL standard, the start, minimum, maximum, and increment values are returned as character strings.
