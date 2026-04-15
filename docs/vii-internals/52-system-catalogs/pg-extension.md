---
title: "52.22. pg_extension"
id: catalog-pg-extension
---

## pg_extension

The catalog pg_extension stores information about the installed extensions.
See [Packaging Related Objects into an Extension](braised:ref/extend-extensions) for details about extensions.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extname `name`

   Name of the extension
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the extension
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   Schema containing the extension\'s exported objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extrelocatable `bool`

   True if extension can be relocated to another schema
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extversion `text`

   Version name for the extension
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extconfig `oid[]` (references [pg_class](#catalog-pg-class).oid)

   Array of `regclass` OIDs for the extension\'s configuration table(s), or `NULL` if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   extcondition `text[]`

   Array of `WHERE`-clause filter conditions for the extension\'s configuration table(s), or `NULL` if none
  :::{/cell}
  :::{/row}
:::{/table}

: pg_extension Columns

Note that unlike most catalogs with a "namespace" column, extnamespace is not meant to imply that the extension belongs to that schema. Extension names are never schema-qualified. Rather, extnamespace indicates the schema that contains most or all of the extension\'s objects. If extrelocatable is true, then this schema must in fact contain all schema-qualifiable objects belonging to the extension.
