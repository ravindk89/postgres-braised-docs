---
title: "52.53. pg_statistic_ext_data"
id: catalog-pg-statistic-ext-data
---

## pg_statistic_ext_data

The catalog pg_statistic_ext_data holds data for extended planner statistics defined in [pg_statistic_ext](#catalog-pg-statistic-ext).
Each row in this catalog corresponds to a statistics object created with [`CREATE STATISTICS`](#sql-createstatistics).

Normally there is one entry, with stxdinherit = `false`, for each statistics object that has been analyzed.
If the table has inheritance children or partitions, a second entry with stxdinherit = `true` is also created.
This row represents the statistics object over the inheritance tree, i.e., statistics for the data you\'d see with `SELECT * FROM table*`, whereas the stxdinherit = `false` row represents the results of `SELECT * FROM ONLY table`.

Like [pg_statistic](#catalog-pg-statistic), pg_statistic_ext_data should not be readable by the public, since the contents might be considered sensitive. (Example: most common combinations of values in columns might be quite interesting.) [pg_stats_ext](#view-pg-stats-ext) is a publicly readable view on pg_statistic_ext_data (after joining with [pg_statistic_ext](#catalog-pg-statistic-ext)) that only exposes information about tables the current user owns.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxoid `oid` (references [pg_statistic_ext](#catalog-pg-statistic-ext).oid)

   Extended statistics object containing the definition for this data
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxdinherit `bool`

   If true, the stats include values from child tables, not just the values in the specified relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxdndistinct `pg_ndistinct`

   N-distinct counts, serialized as pg_ndistinct type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxddependencies `pg_dependencies`

   Functional dependency statistics, serialized as pg_dependencies type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxdmcv `pg_mcv_list`

   MCV (most-common values) list statistics, serialized as pg_mcv_list type
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   stxdexpr `pg_statistic[]`

   Per-expression statistics, serialized as an array of pg_statistic type
  :::{/cell}
  :::{/row}
:::{/table}

: pg_statistic_ext_data Columns
