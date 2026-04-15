---
title: "53.21. pg_roles"
id: view-pg-roles
---

## pg_roles

The view pg_roles provides access to information about database roles.
This is simply a publicly readable view of [pg_authid](#catalog-pg-authid) that blanks out the password field.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolname `name`

   Role name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolsuper `bool`

   Role has superuser privileges
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolinherit `bool`

   Role automatically inherits privileges of roles it is a member of
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolcreaterole `bool`

   Role can create more roles
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolcreatedb `bool`

   Role can create databases
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolcanlogin `bool`

   Role can log in. That is, this role can be given as the initial session authorization identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolreplication `bool`

   Role is a replication role. A replication role can initiate replication connections and create and drop replication slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolconnlimit `int4`

   For roles that can log in, this sets maximum number of concurrent connections this role can make. -1 means no limit.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolpassword `text`

   Not the password (always reads as `********`)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolvaliduntil `timestamptz`

   Password expiry time (only used for password authentication); null if no expiration
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolbypassrls `bool`

   Role bypasses every row-level security policy, see [Row Security Policies](braised:ref/ddl-rowsecurity) for more information.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rolconfig `text[]`

   Role-specific defaults for run-time configuration variables
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of role
  :::{/cell}
  :::{/row}
:::{/table}

: pg_roles Columns
