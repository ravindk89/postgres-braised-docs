---
title: "35.5. applicable_roles"
id: infoschema-applicable-roles
---

## `applicable_roles`

The view `applicable_roles` identifies all roles whose privileges the current user can use.
This means there is some chain of role grants from the current user to the role in question.
The current user itself is also an applicable role.
The set of applicable roles is generally used for permission checking.

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

   `YES` if the grantee has the admin option on the role, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: applicable_roles Columns
