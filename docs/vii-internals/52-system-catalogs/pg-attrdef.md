---
title: "52.6. pg_attrdef"
id: catalog-pg-attrdef
---

## pg_attrdef

The catalog pg_attrdef stores column default expressions and generation expressions.
The main information about columns is stored in [pg_attribute](#catalog-pg-attribute).
Only columns for which a default expression or generation expression has been explicitly set will have an entry here.

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
   adrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The table this column belongs to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   adnum `int2` (references [pg_attribute](#catalog-pg-attribute).attnum)

   The number of the column
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   adbin `pg_node_tree`

   The column default or generation expression, in `nodeToString()` representation. Use `pg_get_expr(adbin, adrelid)` to convert it to an SQL expression.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_attrdef Columns
