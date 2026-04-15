---
title: "52.27. pg_inherits"
id: catalog-pg-inherits
---

## pg_inherits

The catalog pg_inherits records information about table and index inheritance hierarchies.
There is one entry for each direct parent-child table or index relationship in the database. (Indirect inheritance can be determined by following chains of entries.)

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inhrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the child table or index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inhparent `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the parent table or index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inhseqno `int4`

   If there is more than one direct parent for a child table (multiple inheritance), this number tells the order in which the inherited columns are to be arranged. The count starts at 1.

   Indexes cannot have multiple inheritance, since they can only inherit when using declarative partitioning.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inhdetachpending `bool`

   `true` for a partition that is in the process of being detached; `false` otherwise.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_inherits Columns
