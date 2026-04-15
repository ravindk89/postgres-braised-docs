---
title: "52.41. pg_publication_namespace"
id: catalog-pg-publication-namespace
---

## pg_publication_namespace

The catalog pg_publication_namespace contains the mapping between schemas and publications in the database.
This is a many-to-many mapping.

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
   pnpubid `oid` (references [pg_publication](#catalog-pg-publication).oid)

   Reference to publication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pnnspid `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   Reference to schema
  :::{/cell}
  :::{/row}
:::{/table}

: pg_publication_namespace Columns
