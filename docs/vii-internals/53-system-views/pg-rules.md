---
title: "53.22. pg_rules"
id: view-pg-rules
---

## pg_rules

The view pg_rules provides access to useful information about query rewrite rules.

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

   Name of table the rule is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rulename `name` (references [pg_rewrite](#catalog-pg-rewrite).rulename)

   Name of rule
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   definition `text`

   Rule definition (a reconstructed creation command)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_rules Columns

The pg_rules view excludes the `ON SELECT` rules of views and materialized views; those can be seen in [pg_views](#view-pg-views) and [pg_matviews](#view-pg-matviews).
