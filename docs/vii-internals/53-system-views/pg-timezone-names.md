---
title: "53.34. pg_timezone_names"
id: view-pg-timezone-names
---

## pg_timezone_names

The view pg_timezone_names provides a list of time zone names that are recognized by `SET TIMEZONE`, along with their associated abbreviations, UTC offsets, and daylight-savings status. (Technically, PostgreSQL does not use UTC because leap seconds are not handled.) Unlike the abbreviations shown in [pg_timezone_abbrevs](#view-pg-timezone-abbrevs), many of these names imply a set of daylight-savings transition date rules.
Therefore, the associated information changes across local DST boundaries.
The displayed information is computed based on the current value of `CURRENT_TIMESTAMP`.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `text`

   Time zone name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   abbrev `text`

   Time zone abbreviation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   utc_offset `interval`

   Offset from UTC (positive means east of Greenwich)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_dst `bool`

   True if currently observing daylight savings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_timezone_names Columns
