---
title: "53.26. pg_shadow"
id: view-pg-shadow
---

## pg_shadow

The view pg_shadow exists for backwards compatibility: it emulates a catalog that existed in PostgreSQL before version 8.1.
It shows properties of all roles that are marked as rolcanlogin in [pg_authid](#catalog-pg-authid).

The name stems from the fact that this table should not be readable by the public since it contains passwords. [pg_user](#view-pg-user) is a publicly readable view on pg_shadow that blanks out the password field.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usename `name` (references [pg_authid](#catalog-pg-authid).rolname)

   User name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usesysid `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of this user
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usecreatedb `bool`

   User can create databases
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usesuper `bool`

   User is a superuser
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   userepl `bool`

   User can initiate streaming replication and put the system in and out of backup mode.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usebypassrls `bool`

   User bypasses every row-level security policy, see [Row Security Policies](braised:ref/ddl-rowsecurity) for more information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   passwd `text`

   Encrypted password; null if none. See [pg_authid](#catalog-pg-authid) for details of how encrypted passwords are stored.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   valuntil `timestamptz`

   Password expiry time (only used for password authentication)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   useconfig `text[]`

   Session defaults for run-time configuration variables
  :::{/cell}
  :::{/row}
:::{/table}

: pg_shadow Columns
