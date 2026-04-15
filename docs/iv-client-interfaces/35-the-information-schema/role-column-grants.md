---
title: "35.35. role_column_grants"
id: infoschema-role-column-grants
---

## `role_column_grants`

The view `role_column_grants` identifies all privileges granted on columns where the grantor or grantee is a currently enabled role.
Further information can be found under `column_privileges`.
The only effective difference between this view and `column_privileges` is that this view omits columns that have been made accessible to the current user by way of a grant to `PUBLIC`.

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

   Name of the role that granted the privilege
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grantee `sql_identifier`

   Name of the role that the privilege was granted to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database that contains the table that contains the column (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table that contains the column
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table that contains the column
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   column_name `sql_identifier`

   Name of the column
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privilege_type `character_data`

   Type of the privilege: `SELECT`, `INSERT`, `UPDATE`, or `REFERENCES`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   `YES` if the privilege is grantable, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: role_column_grants Columns
