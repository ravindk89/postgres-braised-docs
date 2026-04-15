---
title: "9.31. Statistics Information Functions"
id: functions-statistics
---

## Statistics Information Functions

PostgreSQL provides a function to inspect complex statistics defined using the `CREATE STATISTICS` command.

### Inspecting MCV Lists

pg_mcv_list_items

(

pg_mcv_list

)

setof record

`pg_mcv_list_items` returns a set of records describing all items stored in a multi-column MCV list.
It returns the following columns:

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Type
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `index`
  :::{/cell}
  :::{.cell}
  `integer`
  :::{/cell}
  :::{.cell}
  index of the item in the MCV list
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `values`
  :::{/cell}
  :::{.cell}
  `text[]`
  :::{/cell}
  :::{.cell}
  values stored in the MCV item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `nulls`
  :::{/cell}
  :::{.cell}
  `boolean[]`
  :::{/cell}
  :::{.cell}
  flags identifying `NULL` values
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `frequency`
  :::{/cell}
  :::{.cell}
  `double precision`
  :::{/cell}
  :::{.cell}
  frequency of this MCV item
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `base_frequency`
  :::{/cell}
  :::{.cell}
  `double precision`
  :::{/cell}
  :::{.cell}
  base frequency of this MCV item
  :::{/cell}
  :::{/row}
:::{/table}

The `pg_mcv_list_items` function can be used like this:

    SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                    pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';

Values of the `pg_mcv_list` type can be obtained only from the pg_statistic_ext_data.stxdmcv column.
