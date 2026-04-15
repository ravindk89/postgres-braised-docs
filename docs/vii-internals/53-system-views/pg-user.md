---
title: "53.35. pg_user"
id: view-pg-user
---

## pg_user

The view pg_user provides access to information about database users.
This is simply a publicly readable view of [pg_shadow](#view-pg-shadow) that blanks out the password field.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usename `name`

   User name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   usesysid `oid`

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

   Not the password (always reads as `********`)
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

: pg_user Columns
