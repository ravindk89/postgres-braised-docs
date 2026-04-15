---
title: "35.4. administrable_role_​authorizations"
id: infoschema-administrable-role-authorizations
---

## `administrable_role_​authorizations`

The view `administrable_role_authorizations` identifies all roles that the current user has the admin option for.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantee `sql_identifier`

   Name of the role to which this role membership was granted (can be the current user, or a different role in case of nested role memberships)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   role_name `sql_identifier`

   Name of a role
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   Always `YES`
  :::{/cell}
  :::{/row}
:::{/table}

: administrable_role_authorizations Columns
