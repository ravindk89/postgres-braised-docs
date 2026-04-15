---
title: "52.29. pg_language"
id: catalog-pg-language
---

## pg_language

The catalog pg_language registers languages in which you can write functions or stored procedures.
See [CREATE LANGUAGE](braised:ref/sql-createlanguage) and [Procedural Languages](#procedural-languages) for more information about language handlers.

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
   lanname `name`

   Name of the language
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the language
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanispl `bool`

   This is false for internal languages (such as SQL) and true for user-defined languages. Currently, pg_dump still uses this to determine which languages need to be dumped, but this might be replaced by a different mechanism in the future.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanpltrusted `bool`

   True if this is a trusted language, which means that it is believed not to grant access to anything outside the normal SQL execution environment. Only superusers can create functions in untrusted languages.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanplcallfoid `oid` (references [pg_proc](#catalog-pg-proc).oid)

   For noninternal languages this references the language handler, which is a special function that is responsible for executing all functions that are written in the particular language. Zero for internal languages.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   laninline `oid` (references [pg_proc](#catalog-pg-proc).oid)

   This references a function that is responsible for executing "inline" anonymous code blocks ([DO](braised:ref/sql-do) blocks). Zero if inline blocks are not supported.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanvalidator `oid` (references [pg_proc](#catalog-pg-proc).oid)

   This references a language validator function that is responsible for checking the syntax and validity of new functions when they are created. Zero if no validator is provided.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   lanacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_language Columns
