---
title: "52.47. pg_sequence"
id: catalog-pg-sequence
---

## pg_sequence

The catalog pg_sequence contains information about sequences.
Some of the information about sequences, such as the name and the schema, is in [pg_class](#catalog-pg-class)

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for this sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqtypid `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqstart `int8`

   Start value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqincrement `int8`

   Increment value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqmax `int8`

   Maximum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqmin `int8`

   Minimum value of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqcache `int8`

   Cache size of the sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqcycle `bool`

   Whether the sequence cycles
  :::{/cell}
  :::{/row}
:::{/table}

: pg_sequence Columns
