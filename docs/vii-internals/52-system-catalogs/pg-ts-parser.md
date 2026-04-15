---
title: "52.62. pg_ts_parser"
id: catalog-pg-ts-parser
---

## pg_ts_parser

The pg_ts_parser catalog contains entries defining text search parsers.
A parser is responsible for splitting input text into lexemes and assigning a token type to each lexeme.
Since a parser must be implemented by C-language-level functions, creation of new parsers is restricted to database superusers.

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
   prsname `name`

   Text search parser name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prsnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this parser
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prsstart `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the parser\'s startup function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prstoken `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the parser\'s next-token function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prsend `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the parser\'s shutdown function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prsheadline `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the parser\'s headline function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prslextype `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the parser\'s lextype function
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ts_parser Columns
