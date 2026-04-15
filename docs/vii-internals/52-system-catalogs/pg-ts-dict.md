---
title: "52.61. pg_ts_dict"
id: catalog-pg-ts-dict
---

## pg_ts_dict

The pg_ts_dict catalog contains entries defining text search dictionaries.
A dictionary depends on a text search template, which specifies all the implementation functions needed; the dictionary itself provides values for the user-settable parameters supported by the template.
This division of labor allows dictionaries to be created by unprivileged users.
The parameters are specified by a text string dictinitoption, whose format and meaning vary depending on the template.

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
   dictname `name`

   Text search dictionary name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dictnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this dictionary
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dictowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the dictionary
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dicttemplate `oid` (references [pg_ts_template](#catalog-pg-ts-template).oid)

   The OID of the text search template for this dictionary
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dictinitoption `text`

   Initialization option string for the template
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ts_dict Columns
