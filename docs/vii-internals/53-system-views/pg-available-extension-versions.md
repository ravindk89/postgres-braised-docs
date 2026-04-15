---
title: "53.4. pg_available_extension_versions"
id: view-pg-available-extension-versions
---

## pg_available_extension_versions

The pg_available_extension_versions view lists the specific extension versions that are available for installation.
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
   version `text`

   Version name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   installed `bool`

   True if this version of this extension is currently installed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   superuser `bool`

   True if only superusers are allowed to install this extension (but see trusted)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   trusted `bool`

   True if the extension can be installed by non-superusers with appropriate privileges
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relocatable `bool`

   True if extension can be relocated to another schema
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schema `name`

   Name of the schema that the extension must be installed into, or `NULL` if partially or fully relocatable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   requires `name[]`

   Names of prerequisite extensions, or `NULL` if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   comment `text`

   Comment string from the extension\'s control file
  :::{/cell}
  :::{/row}
:::{/table}

: pg_available_extension_versions Columns

The pg_available_extension_versions view is read-only.
