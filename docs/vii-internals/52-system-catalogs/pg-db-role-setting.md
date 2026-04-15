---
title: "52.16. pg_db_role_setting"
id: catalog-pg-db-role-setting
---

## pg_db_role_setting

The catalog pg_db_role_setting records the default values that have been set for run-time configuration variables, for each role and database combination.

Unlike most system catalogs, pg_db_role_setting is shared across all databases of a cluster: there is only one copy of pg_db_role_setting per cluster, not one per database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   setdatabase `oid` (references [pg_database](#catalog-pg-database).oid)

   The OID of the database the setting is applicable to, or zero if not database-specific
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   setrole `oid` (references [pg_authid](#catalog-pg-authid).oid)

   The OID of the role the setting is applicable to, or zero if not role-specific
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   setconfig `text[]`

   Defaults for run-time configuration variables
  :::{/cell}
  :::{/row}
:::{/table}

: pg_db_role_setting Columns
