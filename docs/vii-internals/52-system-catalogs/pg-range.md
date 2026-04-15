---
title: "52.43. pg_range"
id: catalog-pg-range
---

## pg_range

The catalog pg_range stores information about range types.
This is in addition to the types\' entries in [pg_type](#catalog-pg-type).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngtypid `oid` (references [pg_type](#catalog-pg-type).oid)

   OID of the range type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngsubtype `oid` (references [pg_type](#catalog-pg-type).oid)

   OID of the element type (subtype) of this range type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngmultitypid `oid` (references [pg_type](#catalog-pg-type).oid)

   OID of the multirange type for this range type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngcollation `oid` (references [pg_collation](#catalog-pg-collation).oid)

   OID of the collation used for range comparisons, or zero if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngsubopc `oid` (references [pg_opclass](#catalog-pg-opclass).oid)

   OID of the subtype\'s operator class used for range comparisons
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngcanonical `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the function to convert a range value into canonical form, or zero if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rngsubdiff `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the function to return the difference between two element values as `double precision`, or zero if none
  :::{/cell}
  :::{/row}
:::{/table}

: pg_range Columns

rngsubopc (plus rngcollation, if the element type is collatable) determines the sort ordering used by the range type. rngcanonical is used when the element type is discrete. rngsubdiff is optional but should be supplied to improve performance of GiST indexes on the range type.
