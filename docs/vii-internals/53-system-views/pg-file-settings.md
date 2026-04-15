---
title: "53.8. pg_file_settings"
id: view-pg-file-settings
---

## pg_file_settings

The view pg_file_settings provides a summary of the contents of the server\'s configuration file(s).
A row appears in this view for each "name = value" entry appearing in the files, with annotations indicating whether the value could be applied successfully.
Additional row(s) may appear for problems not linked to a "name = value" entry, such as syntax errors in the files.

This view is helpful for checking whether planned changes in the configuration files will work, or for diagnosing a previous failure.
Note that this view reports on the *current* contents of the files, not on what was last applied by the server. (The [pg_settings](#view-pg-settings) view is usually sufficient to determine that.)

By default, the pg_file_settings view can be read only by superusers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sourcefile `text`

   Full path name of the configuration file
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sourceline `int4`

   Line number within the configuration file where the entry appears
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   seqno `int4`

   Order in which the entries are processed (1..*n*)                          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `text`

   Configuration parameter name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   setting `text`

   Value to be assigned to the parameter
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   applied `bool`

   True if the value can be applied successfully
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   error `text`

   If not null, an error message indicating why this entry could not be applied
  :::{/cell}
  :::{/row}
:::{/table}

: pg_file_settings Columns

If the configuration file contains syntax errors or invalid parameter names, the server will not attempt to apply any settings from it, and therefore all the applied fields will read as false. In such a case there will be one or more rows with non-null error fields indicating the problem(s). Otherwise, individual settings will be applied if possible. If an individual setting cannot be applied (e.g., invalid value, or the setting cannot be changed after server start) it will have an appropriate message in the error field. Another way that an entry might have applied = false is that it is overridden by a later entry for the same parameter name; this case is not considered an error so nothing appears in the error field.

See [Setting Parameters](braised:ref/config-setting) for more information about the various ways to change run-time parameters.
