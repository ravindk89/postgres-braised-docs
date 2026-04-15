---
title: "35.59. usage_privileges"
id: infoschema-usage-privileges
---

## `usage_privileges`

The view `usage_privileges` identifies `USAGE` privileges granted on various kinds of objects to a currently enabled role or by a currently enabled role.
In PostgreSQL, this currently applies to collations, domains, foreign-data wrappers, foreign servers, and sequences.
There is one row for each combination of object, grantor, and grantee.

Since collations do not have real privileges in PostgreSQL, this view shows implicit non-grantable `USAGE` privileges granted by the owner to `PUBLIC` for all collations.
The other object types, however, show real privileges.

In PostgreSQL, sequences also support `SELECT` and `UPDATE` privileges in addition to the `USAGE` privilege.
These are nonstandard and therefore not visible in the information schema.

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

: usage_privileges Columns
