---
title: "53.3. pg_available_extensions"
id: view-pg-available-extensions
---

## pg_available_extensions

The pg_available_extensions view lists the extensions that are available for installation.
See also the [pg_extension](#catalog-pg-extension) catalog, which shows the extensions currently installed.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `name`

   Extension name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   default_version `text`

   Name of default version, or `NULL` if none is specified
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   installed_version `text`

   Currently installed version of the extension, or `NULL` if not installed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   comment `text`

   Comment string from the extension\'s control file
  :::{/cell}
  :::{/row}
:::{/table}

: pg_available_extensions Columns

The pg_available_extensions view is read-only.
