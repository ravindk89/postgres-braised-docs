---
title: "52.36. pg_parameter_acl"
id: catalog-pg-parameter-acl
---

## pg_parameter_acl

The catalog pg_parameter_acl records configuration parameters for which privileges have been granted to one or more roles.
No entry is made for parameters that have default privileges.

Unlike most system catalogs, pg_parameter_acl is shared across all databases of a cluster: there is only one copy of pg_parameter_acl per cluster, not one per database.

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
   parname `text`

   The name of a configuration parameter for which privileges are granted
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   paracl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_parameter_acl Columns
