---
title: "52.65. pg_user_mapping"
id: catalog-pg-user-mapping
---

## pg_user_mapping

The catalog pg_user_mapping stores the mappings from local user to remote.
Access to this catalog is restricted from normal users, use the view [pg_user_mappings](#view-pg-user-mappings) instead.

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
   umuser `oid` (references [pg_authid](#catalog-pg-authid).oid)

   OID of the local role being mapped, or zero if the user mapping is public
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   umserver `oid` (references [pg_foreign_server](#catalog-pg-foreign-server).oid)

   The OID of the foreign server that contains this mapping
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   umoptions `text[]`

   User mapping specific options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_user_mapping Columns
