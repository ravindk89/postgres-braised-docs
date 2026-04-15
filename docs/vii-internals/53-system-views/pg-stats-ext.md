---
title: "53.30. pg_stats_ext"
id: view-pg-stats-ext
---

## pg_stats_ext

The view pg_stats_ext provides access to information about each extended statistics object in the database, combining information stored in the [pg_statistic_ext](#catalog-pg-statistic-ext) and [pg_statistic_ext_data](#catalog-pg-statistic-ext-data) catalogs.
This view allows access only to rows of [pg_statistic_ext](#catalog-pg-statistic-ext) and [pg_statistic_ext_data](#catalog-pg-statistic-ext-data) that correspond to tables the user owns, and therefore it is safe to allow public read access to this view.

pg_stats_ext is also designed to present the information in a more readable format than the underlying catalogs at the cost that its schema must be extended whenever new types of extended statistics are added to [pg_statistic_ext](#catalog-pg-statistic-ext).

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
   statistics_schemaname `name` (references [pg_namespace](#catalog-pg-namespace).nspname)

   Name of schema containing extended statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   statistics_name `name` (references [pg_statistic_ext](#catalog-pg-statistic-ext).stxname)

   Name of extended statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   statistics_owner `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Owner of the extended statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   attnames `name[]` (references [pg_attribute](#catalog-pg-attribute).attname)

   Names of the columns included in the extended statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   exprs `text[]`

   Expressions included in the extended statistics object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   kinds `char[]`

   Types of extended statistics object enabled for this record
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inherited `bool` (references [pg_statistic_ext_data](#catalog-pg-statistic-ext-data).stxdinherit)

   If true, the stats include values from child tables, not just the values in the specified relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_distinct `pg_ndistinct`

   N-distinct counts for combinations of column values. If greater than zero, the estimated number of distinct values in the combination. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when `ANALYZE` believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.) For example, -1 indicates a unique combination of columns in which the number of distinct combinations is the same as the number of rows.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dependencies `pg_dependencies`

   Functional dependency statistics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_vals `text[]`

   A list of the most common combinations of values in the columns. (Null if no combinations seem to be more common than any others.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_val_nulls `bool[]`

   A list of NULL flags for the most common combinations of values. (Null when most_common_vals is.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_freqs `float8[]`

   A list of the frequencies of the most common combinations, i.e., number of occurrences of each divided by total number of rows. (Null when most_common_vals is.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_base_freqs `float8[]`

   A list of the base frequencies of the most common combinations, i.e., product of per-value frequencies. (Null when most_common_vals is.)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stats_ext Columns

The maximum number of entries in the array fields can be controlled on a column-by-column basis using the [`ALTER TABLE SET STATISTICS`](#sql-altertable) command, or globally by setting the [default_statistics_target (integer)
      
       default_statistics_target configuration parameter](braised:ref/runtime-config-query#default-statistics-target-integer-default-statistics-target-configuration-parameter) run-time parameter.
