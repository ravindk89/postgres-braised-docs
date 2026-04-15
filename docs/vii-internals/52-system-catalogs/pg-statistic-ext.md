---
title: "52.52. pg_statistic_ext"
id: catalog-pg-statistic-ext
---

## pg_statistic_ext

The catalog pg_statistic_ext holds definitions of extended planner statistics.
Each row in this catalog corresponds to a statistics object created with [`CREATE STATISTICS`](#sql-createstatistics).

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
   stxrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   Table containing the columns described by this object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxname `name`

   Name of the statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxkeys `int2vector` (references [pg_attribute](#catalog-pg-attribute).attnum)

   An array of attribute numbers, indicating which table columns are covered by this statistics object; for example a value of `1 3` would mean that the first and the third table columns are covered
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxstattarget `int2`

   stxstattarget controls the level of detail of statistics accumulated for this statistics object by [`ANALYZE`](#sql-analyze). A zero value indicates that no statistics should be collected. A null value says to use the maximum of the statistics targets of the referenced columns, if set, or the system default statistics target. Positive values of stxstattarget determine the target number of "most common values" to collect.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxkind `char[]`

   An array containing codes for the enabled statistics kinds; valid values are: `d` for n-distinct statistics, `f` for functional dependency statistics, `m` for most common values (MCV) list statistics, and `e` for expression statistics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxexprs `pg_node_tree`

   Expression trees (in `nodeToString()` representation) for statistics object attributes that are not simple column references. This is a list with one element per expression. Null if all statistics object attributes are simple references.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_statistic_ext Columns

The pg_statistic_ext entry is filled in completely during [`CREATE STATISTICS`](#sql-createstatistics), but the actual statistical values are not computed then. Subsequent [`ANALYZE`](#sql-analyze) commands compute the desired values and populate an entry in the [pg_statistic_ext_data](#catalog-pg-statistic-ext-data) catalog.
