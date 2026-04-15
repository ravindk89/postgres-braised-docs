---
title: "53.29. pg_stats"
id: view-pg-stats
---

## pg_stats

The view pg_stats provides access to the information stored in the [pg_statistic](#catalog-pg-statistic) catalog.
This view allows access only to rows of [pg_statistic](#catalog-pg-statistic) that correspond to tables the user has permission to read, and therefore it is safe to allow public read access to this view.

pg_stats is also designed to present the information in a more readable format than the underlying catalog at the cost that its schema must be extended whenever new slot types are defined for [pg_statistic](#catalog-pg-statistic).

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
   attname `name` (references [pg_attribute](#catalog-pg-attribute).attname)

   Name of column described by this row
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inherited `bool`

   If true, this row includes values from child tables, not just the values in the specified table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   null_frac `float4`

   Fraction of column entries that are null
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   avg_width `int4`

   Average width in bytes of column\'s entries
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   n_distinct `float4`

   If greater than zero, the estimated number of distinct values in the column. If less than zero, the negative of the number of distinct values divided by the number of rows. (The negated form is used when `ANALYZE` believes that the number of distinct values is likely to increase as the table grows; the positive form is used when the column seems to have a fixed number of possible values.) For example, -1 indicates a unique column in which the number of distinct values is the same as the number of rows.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_vals `anyarray`

   A list of the most common values in the column. (Null if no values seem to be more common than any others.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_freqs `float4[]`

   A list of the frequencies of the most common values, i.e., number of occurrences of each divided by total number of rows. (Null when most_common_vals is.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   histogram_bounds `anyarray`

   A list of values that divide the column\'s values into groups of approximately equal population. The values in most_common_vals, if present, are omitted from this histogram calculation. (This column is null if the column data type does not have a `<` operator or if the most_common_vals list accounts for the entire population.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   correlation `float4`

   Statistical correlation between physical row ordering and logical ordering of the column values. This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the column will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk. (This column is null if the column data type does not have a `<` operator.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_elems `anyarray`

   A list of non-null element values most often appearing within values of the column. (Null for scalar types.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   most_common_elem_freqs `float4[]`

   A list of the frequencies of the most common element values, i.e., the fraction of rows containing at least one instance of the given value. Two or three additional values follow the per-element frequencies; these are the minimum and maximum of the preceding per-element frequencies, and optionally the frequency of null elements. (Null when most_common_elems is.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   elem_count_histogram `float4[]`

   A histogram of the counts of distinct non-null element values within the values of the column, followed by the average number of distinct non-null elements. (Null for scalar types.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   range_length_histogram `anyarray`

   A histogram of the lengths of non-empty and non-null range values of a range type column. (Null for non-range types.)

   This histogram is calculated using the `subtype_diff` range function regardless of whether range bounds are inclusive.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   range_empty_frac `float4`

   Fraction of column entries whose values are empty ranges. (Null for non-range types.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   range_bounds_histogram `anyarray`

   A histogram of lower and upper bounds of non-empty and non-null range values. (Null for non-range types.)

   These two histograms are represented as a single array of ranges, whose lower bounds represent the histogram of lower bounds, and upper bounds represent the histogram of upper bounds.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_stats Columns

The maximum number of entries in the array fields can be controlled on a column-by-column basis using the [`ALTER TABLE SET STATISTICS`](#sql-altertable) command, or globally by setting the [default_statistics_target (integer)
      
       default_statistics_target configuration parameter](braised:ref/runtime-config-query#default-statistics-target-integer-default-statistics-target-configuration-parameter) run-time parameter.
