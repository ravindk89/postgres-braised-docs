---
title: "52.57. pg_transform"
id: catalog-pg-transform
---

## pg_transform

The catalog pg_transform stores information about transforms, which are a mechanism to adapt data types to procedural languages.
See [CREATE TRANSFORM](braised:ref/sql-createtransform) for more information.

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
   trftype `oid` (references [pg_type](#catalog-pg-type).oid)

   OID of the data type this transform is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trflang `oid` (references [pg_language](#catalog-pg-language).oid)

   OID of the language this transform is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trffromsql `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   The OID of the function to use when converting the data type for input to the procedural language (e.g., function parameters). Zero is stored if the default behavior should be used.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trftosql `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   The OID of the function to use when converting output from the procedural language (e.g., return values) to the data type. Zero is stored if the default behavior should be used.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_transform Columns
