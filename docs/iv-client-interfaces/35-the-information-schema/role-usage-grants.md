---
title: "35.39. role_usage_grants"
id: infoschema-role-usage-grants
---

## `role_usage_grants`

The view `role_usage_grants` identifies `USAGE` privileges granted on various kinds of objects where the grantor or grantee is a currently enabled role.
Further information can be found under `usage_privileges`.
The only effective difference between this view and `usage_privileges` is that this view omits objects that have been made accessible to the current user by way of a grant to `PUBLIC`.

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
   object_catalog `sql_identifier`

   Name of the database containing the object (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   object_schema `sql_identifier`

   Name of the schema containing the object, if applicable, else an empty string
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   object_name `sql_identifier`

   Name of the object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   object_type `character_data`

   `COLLATION` or `DOMAIN` or `FOREIGN DATA WRAPPER` or `FOREIGN SERVER` or `SEQUENCE`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privilege_type `character_data`

   Always `USAGE`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   `YES` if the privilege is grantable, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: role_usage_grants Columns
