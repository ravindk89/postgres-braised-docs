---
title: "53.14. pg_matviews"
id: view-pg-matviews
---

## pg_matviews

The view pg_matviews provides access to useful information about each materialized view in the database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name` (references [pg_namespace](#catalog-pg-namespace).nspname)

   Name of schema containing materialized view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   matviewname `name` (references [pg_class](#catalog-pg-class).relname)

   Name of materialized view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   matviewowner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of materialized view\'s owner
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablespace `name` (references [pg_tablespace](#catalog-pg-tablespace).spcname)

   Name of tablespace containing materialized view (null if default for database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hasindexes `bool`

   True if materialized view has (or recently had) any indexes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ispopulated `bool`

   True if materialized view is currently populated
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   definition `text`

   Materialized view definition (a reconstructed [SELECT](braised:ref/sql-select) query)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_matviews Columns
