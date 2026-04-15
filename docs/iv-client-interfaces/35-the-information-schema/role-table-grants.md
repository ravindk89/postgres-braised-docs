---
title: "35.37. role_table_grants"
id: infoschema-role-table-grants
---

## `role_table_grants`

The view `role_table_grants` identifies all privileges granted on tables or views where the grantor or grantee is a currently enabled role.
Further information can be found under `table_privileges`.
The only effective difference between this view and `table_privileges` is that this view omits tables that have been made accessible to the current user by way of a grant to `PUBLIC`.

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

   Name of the database that contains the table (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privilege_type `character_data`

   Type of the privilege: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, or `TRIGGER`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_grantable `yes_or_no`

   `YES` if the privilege is grantable, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   with_hierarchy `yes_or_no`

   In the SQL standard, `WITH HIERARCHY OPTION` is a separate (sub-)privilege allowing certain operations on table inheritance hierarchies. In PostgreSQL, this is included in the `SELECT` privilege, so this column shows `YES` if the privilege is `SELECT`, else `NO`.
  :::{/cell}
  :::{/row}
:::{/table}

: role_table_grants Columns
