---
title: "53.36. pg_user_mappings"
id: view-pg-user-mappings
---

## pg_user_mappings

The view pg_user_mappings provides access to information about user mappings.
This is essentially a publicly readable view of [pg_user_mapping](#catalog-pg-user-mapping) that leaves out the options field if the user has no rights to use it.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   umid `oid` (references [pg_user_mapping](#catalog-pg-user-mapping).oid)

   OID of the user mapping
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvid `oid` (references [pg_foreign_server](#catalog-pg-foreign-server).oid)

   The OID of the foreign server that contains this mapping
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   srvname `name` (references [pg_foreign_server](#catalog-pg-foreign-server).srvname)

   Name of the foreign server
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
   usename `name`

   Name of the local user to be mapped
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   umoptions `text[]`

   User mapping specific options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_user_mappings Columns

To protect password information stored as a user mapping option, the umoptions column will read as null unless one of the following applies:

-   current user is the user being mapped, and owns the server or holds `USAGE` privilege on it

-   current user is the server owner and mapping is for `PUBLIC`

-   current user is a superuser
