---
title: "52.14. pg_conversion"
id: catalog-pg-conversion
---

## pg_conversion

The catalog pg_conversion describes encoding conversion functions.
See [CREATE CONVERSION](braised:ref/sql-createconversion) for more information.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conname `name`

   Conversion name (unique within a namespace)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   connamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this conversion
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the conversion
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conforencoding `int4`

   Source encoding ID ([`pg_encoding_to_char()`](#pg-encoding-to-char) can translate this number to the encoding name)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   contoencoding `int4`

   Destination encoding ID ([`pg_encoding_to_char()`](#pg-encoding-to-char) can translate this number to the encoding name)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conproc `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Conversion function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   condefault `bool`

   True if this is the default conversion
  :::{/cell}
  :::{/row}
:::{/table}

: pg_conversion Columns
