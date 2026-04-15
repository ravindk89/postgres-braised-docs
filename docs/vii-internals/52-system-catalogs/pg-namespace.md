---
title: "52.32. pg_namespace"
id: catalog-pg-namespace
---

## pg_namespace

The catalog pg_namespace stores namespaces.
A namespace is the structure underlying SQL schemas: each namespace can have a separate collection of relations, types, etc. without name conflicts.

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
   nspname `name`

   Name of the namespace
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   nspowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the namespace
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   nspacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_namespace Columns
