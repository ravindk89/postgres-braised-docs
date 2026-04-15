---
title: "53.33. pg_timezone_abbrevs"
id: view-pg-timezone-abbrevs
---

## pg_timezone_abbrevs

The view pg_timezone_abbrevs provides a list of time zone abbreviations that are currently recognized by the datetime input routines.
The contents of this view change when the [TimeZone (string)
      
       TimeZone configuration parameter
      
      time zone](braised:ref/runtime-config-client#timezone-string-timezone-configuration-parameter-time-zone) or [timezone_abbreviations (string)
      
       timezone_abbreviations configuration parameter
      
      time zone names](braised:ref/runtime-config-client#timezone-abbreviations-string-timezone-abbreviations-configuration-parameter-time-zone-names) run-time parameters are modified.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
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

   True if this is a daylight-savings abbreviation
  :::{/cell}
  :::{/row}
:::{/table}

: pg_timezone_abbrevs Columns

While most timezone abbreviations represent fixed offsets from UTC, there are some that have historically varied in value (see [B.4. Date/Time Configuration Files](braised:ref/datetime-config-files) for more information). In such cases this view presents their current meaning.
