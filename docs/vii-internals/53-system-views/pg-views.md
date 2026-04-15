---
title: "53.37. pg_views"
id: view-pg-views
---

## pg_views

The view pg_views provides access to useful information about each view in the database.

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

   Name of schema containing view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   viewname `name` (references [pg_class](#catalog-pg-class).relname)

   Name of view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   viewowner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of view\'s owner
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   definition `text`

   View definition (a reconstructed [SELECT](braised:ref/sql-select) query)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_views Columns
