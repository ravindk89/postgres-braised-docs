---
title: "52.45. pg_rewrite"
id: catalog-pg-rewrite
---

## pg_rewrite

The catalog pg_rewrite stores rewrite rules for tables and views.

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
   rulename `name`

   Rule name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ev_class `oid` (references [pg_class](#catalog-pg-class).oid)

   The table this rule is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ev_type `char`

   Event type that the rule is for: 1 = [SELECT](braised:ref/sql-select), 2 = [UPDATE](braised:ref/sql-update), 3 = [INSERT](braised:ref/sql-insert), 4 = [DELETE](braised:ref/sql-delete)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ev_enabled `char`

   Controls in which [session_replication_role (enum)
      
       session_replication_role configuration parameter](braised:ref/runtime-config-client#session-replication-role-enum-session-replication-role-configuration-parameter) modes the rule fires. `O` = rule fires in "origin" and "local" modes, `D` = rule is disabled, `R` = rule fires in "replica" mode, `A` = rule fires always.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_instead `bool`

   True if the rule is an `INSTEAD` rule
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ev_qual `pg_node_tree`

   Expression tree (in the form of a `nodeToString()` representation) for the rule\'s qualifying condition
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ev_action `pg_node_tree`

   Query tree (in the form of a `nodeToString()` representation) for the rule\'s action
  :::{/cell}
  :::{/row}
:::{/table}

: pg_rewrite Columns

:::{.callout type="note"}
`pg_class.relhasrules` must be true if a table has any rules in this catalog.
:::
