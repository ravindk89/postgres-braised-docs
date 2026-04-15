---
title: "52.31. pg_largeobject_metadata"
id: catalog-pg-largeobject-metadata
---

## pg_largeobject_metadata

The catalog pg_largeobject_metadata holds metadata associated with large objects.
The actual large object data is stored in [pg_largeobject](#catalog-pg-largeobject).

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
   lomowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the large object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lomacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_largeobject_metadata Columns
