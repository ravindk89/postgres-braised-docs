---
title: "53.11. pg_ident_file_mappings"
id: view-pg-ident-file-mappings
---

## pg_ident_file_mappings

The view pg_ident_file_mappings provides a summary of the contents of the client user name mapping configuration file, [`pg_ident.conf`](#auth-username-maps).
A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the map could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure.
Note that this view reports on the *current* contents of the file, not on what was last loaded by the server.

By default, the pg_ident_file_mappings view can be read only by superusers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   map_number `int4`

   Number of this map, in priority order, if valid, otherwise `NULL`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   file_name `text`

   Name of the file containing this map
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   line_number `int4`

   Line number of this map in `file_name`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   map_name `text`

   Name of the map
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   sys_name `text`

   Detected user name of the client
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pg_username `text`

   Requested PostgreSQL user name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   error `text`

   If not `NULL`, an error message indicating why this line could not be processed
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ident_file_mappings Columns

Usually, a row reflecting an incorrect entry will have values for only the line_number and error fields.

See [Client Authentication](#client-authentication) for more information about client authentication configuration.
