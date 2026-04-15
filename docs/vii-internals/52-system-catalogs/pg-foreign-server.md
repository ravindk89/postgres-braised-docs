---
title: "52.24. pg_foreign_server"
id: catalog-pg-foreign-server
---

## pg_foreign_server

The catalog pg_foreign_server stores foreign server definitions.
A foreign server describes a source of external data, such as a remote server.
Foreign servers are accessed via foreign-data wrappers.

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
   srvname `name`

   Name of the foreign server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the foreign server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvfdw `oid` (references [pg_foreign_data_wrapper](#catalog-pg-foreign-data-wrapper).oid)

   OID of the foreign-data wrapper of this foreign server
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvtype `text`

   Type of the server (optional)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvversion `text`

   Version of the server (optional)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvoptions `text[]`

   Foreign server specific options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_foreign_server Columns
