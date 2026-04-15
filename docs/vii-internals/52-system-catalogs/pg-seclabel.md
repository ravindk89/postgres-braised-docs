---
title: "52.46. pg_seclabel"
id: catalog-pg-seclabel
---

## pg_seclabel

The catalog pg_seclabel stores security labels on database objects.
Security labels can be manipulated with the [`SECURITY LABEL`](#sql-security-label) command.
For an easier way to view security labels, see [pg_seclabels](braised:ref/view-pg-seclabels).

See also [pg_shseclabel](#catalog-pg-shseclabel), which performs a similar function for security labels of database objects that are shared across a database cluster.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objoid `oid` (references any OID column)

   The OID of the object this security label pertains to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   classoid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the system catalog this object appears in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objsubid `int4`

   For a security label on a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   provider `text`

   The label provider associated with this label.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   label `text`

   The security label applied to this object.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_seclabel Columns
