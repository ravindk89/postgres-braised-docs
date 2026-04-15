---
title: "35.25. enabled_roles"
id: infoschema-enabled-roles
---

## `enabled_roles`

The view `enabled_roles` identifies the currently "enabled roles".
The enabled roles are recursively defined as the current user together with all roles that have been granted to the enabled roles with automatic inheritance.
In other words, these are all roles that the current user has direct or indirect, automatically inheriting membership in.

For permission checking, the set of "applicable roles" is applied, which can be broader than the set of enabled roles.
So generally, it is better to use the view `applicable_roles` instead of this one; See [applicable_roles](braised:ref/infoschema-applicable-roles) for details on `applicable_roles` view.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   role_name `sql_identifier`

   Name of a role
  :::{/cell}
  :::{/row}
:::{/table}

: enabled_roles Columns
