---
title: "52.63. pg_ts_template"
id: catalog-pg-ts-template
---

## pg_ts_template

The pg_ts_template catalog contains entries defining text search templates.
A template is the implementation skeleton for a class of text search dictionaries.
Since a template must be implemented by C-language-level functions, creation of new templates is restricted to database superusers.

PostgreSQL\'s text search features are described at length in [Full Text Search](#full-text-search).

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
   tmplname `name`

   Text search template name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tmplnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this template
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tmplinit `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the template\'s initialization function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tmpllexize `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the template\'s lexize function
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ts_template Columns
