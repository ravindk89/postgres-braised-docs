---
title: "53.6. pg_config"
id: view-pg-config
---

## pg_config

The view pg_config describes the compile-time configuration parameters of the currently installed version of PostgreSQL.
It is intended, for example, to be used by software packages that want to interface to PostgreSQL to facilitate finding the required header files and libraries.
It provides the same basic information as the [pg_config](braised:ref/app-pgconfig) PostgreSQL client application.

By default, the pg_config view can be read only by superusers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `text`

   The parameter name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   setting `text`

   The parameter value
  :::{/cell}
  :::{/row}
:::{/table}

: pg_config Columns
