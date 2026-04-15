---
title: "52.56. pg_tablespace"
id: catalog-pg-tablespace
---

## pg_tablespace

The catalog pg_tablespace stores information about the available tablespaces.
Tables can be placed in particular tablespaces to aid administration of disk layout.

Unlike most system catalogs, pg_tablespace is shared across all databases of a cluster: there is only one copy of pg_tablespace per cluster, not one per database.

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
   spcname `name`

   Tablespace name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spcowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the tablespace, usually the user who created it
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spcacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   spcoptions `text[]`

   Tablespace-level options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_tablespace Columns
