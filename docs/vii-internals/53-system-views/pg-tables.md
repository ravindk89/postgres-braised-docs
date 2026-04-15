---
title: "53.32. pg_tables"
id: view-pg-tables
---

## pg_tables

The view pg_tables provides access to useful information about each table in the database.

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

   Name of schema containing table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablename `name` (references [pg_class](#catalog-pg-class).relname)

   Name of table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tableowner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of table\'s owner
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablespace `name` (references [pg_tablespace](#catalog-pg-tablespace).spcname)

   Name of tablespace containing table (null if default for database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hasindexes `bool` (references [pg_class](#catalog-pg-class).relhasindex)

   True if table has (or recently had) any indexes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hasrules `bool` (references [pg_class](#catalog-pg-class).relhasrules)

   True if table has (or once had) rules
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   hastriggers `bool` (references [pg_class](#catalog-pg-class).relhastriggers)

   True if table has (or once had) triggers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rowsecurity `bool` (references [pg_class](#catalog-pg-class).relrowsecurity)

   True if row security is enabled on the table
  :::{/cell}
  :::{/row}
:::{/table}

: pg_tables Columns
