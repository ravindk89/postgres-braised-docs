---
title: "53.23. pg_seclabels"
id: view-pg-seclabels
---

## pg_seclabels

The view pg_seclabels provides information about security labels.
It as an easier-to-query version of the [pg_seclabel](#catalog-pg-seclabel) catalog.

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
   objtype `text`

   The type of object to which this label applies, as text.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace for this object, if applicable; otherwise NULL.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objname `text`

   The name of the object to which this label applies, as text.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   provider `text` (references [pg_seclabel](#catalog-pg-seclabel).provider)

   The label provider associated with this label.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   label `text` (references [pg_seclabel](#catalog-pg-seclabel).label)

   The security label applied to this object.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_seclabels Columns
