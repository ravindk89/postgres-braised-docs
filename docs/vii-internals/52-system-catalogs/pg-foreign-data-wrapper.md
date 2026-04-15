---
title: "52.23. pg_foreign_data_wrapper"
id: catalog-pg-foreign-data-wrapper
---

## pg_foreign_data_wrapper

The catalog pg_foreign_data_wrapper stores foreign-data wrapper definitions.
A foreign-data wrapper is the mechanism by which external data, residing on foreign servers, is accessed.

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
   fdwname `name`

   Name of the foreign-data wrapper
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fdwowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the foreign-data wrapper
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fdwhandler `oid` (references [pg_proc](#catalog-pg-proc).oid)

   References a handler function that is responsible for supplying execution routines for the foreign-data wrapper. Zero if no handler is provided
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fdwvalidator `oid` (references [pg_proc](#catalog-pg-proc).oid)

   References a validator function that is responsible for checking the validity of the options given to the foreign-data wrapper, as well as options for foreign servers and user mappings using the foreign-data wrapper. Zero if no validator is provided
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fdwacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   fdwoptions `text[]`

   Foreign-data wrapper specific options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
:::{/table}

: pg_foreign_data_wrapper Columns
