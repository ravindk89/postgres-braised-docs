---
title: "35.38. role_udt_grants"
id: infoschema-role-udt-grants
---

## `role_udt_grants`

The view `role_udt_grants` is intended to identify `USAGE` privileges granted on user-defined types where the grantor or grantee is a currently enabled role.
Further information can be found under `udt_privileges`.
The only effective difference between this view and `udt_privileges` is that this view omits objects that have been made accessible to the current user by way of a grant to `PUBLIC`.
Since data types do not have real privileges in PostgreSQL, but only an implicit grant to `PUBLIC`, this view is empty.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantor `sql_identifier`

   The name of the role that granted the privilege
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantee `sql_identifier`

   The name of the role that the privilege was granted to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_catalog `sql_identifier`

   Name of the database containing the type (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_schema `sql_identifier`

   Name of the schema containing the type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   udt_name `sql_identifier`

   Name of the type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privilege_type `character_data`

   Always `TYPE USAGE`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   `YES` if the privilege is grantable, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: role_udt_grants Columns
