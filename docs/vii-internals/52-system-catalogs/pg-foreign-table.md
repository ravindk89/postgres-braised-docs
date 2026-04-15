---
title: "52.25. pg_foreign_table"
id: catalog-pg-foreign-table
---

## pg_foreign_table

The catalog pg_foreign_table contains auxiliary information about foreign tables.
A foreign table is primarily represented by a [pg_class](#catalog-pg-class) entry, just like a regular table.
Its pg_foreign_table entry contains the information that is pertinent only to foreign tables and not any other kind of relation.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ftrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for this foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ftserver `oid` (references [pg_foreign_server](#catalog-pg-foreign-server).oid)

   OID of the foreign server for this foreign table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ftoptions `text[]`

   Foreign table options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_foreign_table Columns
