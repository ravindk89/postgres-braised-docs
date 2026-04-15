---
title: "52.9. pg_auth_members"
id: catalog-pg-auth-members
---

## pg_auth_members

The catalog pg_auth_members shows the membership relations between roles.
Any non-circular set of relationships is allowed.

Because user identities are cluster-wide, pg_auth_members is shared across all databases of a cluster: there is only one copy of pg_auth_members per cluster, not one per database.

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
   roleid `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of a role that has a member
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   member `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of a role that is a member of roleid
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantor `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of the role that granted this membership
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   admin_option `bool`

   True if member can grant membership in roleid to others
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inherit_option `bool`

   True if the member automatically inherits the privileges of the granted role
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   set_option `bool`

   True if the member can [`SET ROLE`](#sql-set-role) to the granted role
  :::{/cell}
  :::{/row}
:::{/table}

: pg_auth_members Columns
