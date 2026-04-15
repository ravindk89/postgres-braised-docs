---
title: "53.12. pg_indexes"
id: view-pg-indexes
---

## pg_indexes

The view pg_indexes provides access to useful information about each index in the database.

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

   Name of schema containing table and index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablename `name` (references [pg_class](#catalog-pg-class).relname)

   Name of table the index is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexname `name` (references [pg_class](#catalog-pg-class).relname)

   Name of index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablespace `name` (references [pg_tablespace](#catalog-pg-tablespace).spcname)

   Name of tablespace containing index (null if default for database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexdef `text`

   Index definition (a reconstructed [CREATE INDEX](braised:ref/sql-createindex) command)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_indexes Columns
