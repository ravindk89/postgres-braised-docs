---
title: "8.2. Monetary Types"
id: datatype-money
---

## Monetary Types

The `money` type stores a currency amount with a fixed fractional precision; see Monetary Types.
The fractional precision is determined by the database\'s [lc_monetary (string)
      
       lc_monetary configuration parameter](braised:ref/runtime-config-client#lc-monetary-string-lc-monetary-configuration-parameter) setting. The range shown in the table assumes there are two fractional digits. Input is accepted in a variety of formats, including integer and floating-point literals, as well as typical currency formatting, such as `'$1,000.00'`. Output is generally in the latter form but depends on the locale.

---------------------------------------------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Storage Size
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{.cell}
  Range
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `money`
  :::{/cell}
  :::{.cell}
  8 bytes
  :::{/cell}
  :::{.cell}
  currency amount
  :::{/cell}
  :::{.cell}
  -92233720368547758.08 to +92233720368547758.07
  :::{/cell}
  :::{/row}
:::{/table}

  ---------------------------------------------------------------------------------------------------------

  : Monetary Types

Since the output of this data type is locale-sensitive, it might not work to load `money` data into a database that has a different setting of `lc_monetary`. To avoid problems, before restoring a dump into a new database make sure `lc_monetary` has the same or equivalent value as in the database that was dumped.

Values of the `numeric`, `int`, and `bigint` data types can be cast to `money`. Conversion from the `real` and `double precision` data types can be done by casting to `numeric` first, for example:

    SELECT '12.34'::float8::numeric::money;

However, this is not recommended. Floating point numbers should not be used to handle money due to the potential for rounding errors.

A `money` value can be cast to `numeric` without loss of precision. Conversion to other types could potentially lose precision, and must also be done in two stages:

    SELECT '52093.89'::money::numeric::float8;

Division of a `money` value by an integer value is performed with truncation of the fractional part towards zero. To get a rounded result, divide by a floating-point value, or cast the `money` value to `numeric` before dividing and back to `money` afterwards. (The latter is preferable to avoid risking precision loss.) When a `money` value is divided by another `money` value, the result is `double precision` (i.e., a pure number, not money); the currency units cancel each other out in the division.
