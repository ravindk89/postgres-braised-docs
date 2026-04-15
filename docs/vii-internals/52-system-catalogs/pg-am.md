---
title: "52.3. pg_am"
id: catalog-pg-am
---

## pg_am

The catalog pg_am stores information about relation access methods.
There is one row for each access method supported by the system.
Currently, only tables and indexes have access methods.
The requirements for table and index access methods are discussed in detail in [Table Access Method Interface Definition](braised:ref/tableam) and [Index Access Method Interface Definition](#index-access-method-interface-definition) respectively.

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
   amname `name`

   Name of the access method
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amhandler `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of a handler function that is responsible for supplying information about the access method
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amtype `char`

   `t` = table (including materialized views), `i` = index.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_am Columns

:::{.callout type="note"}
Before PostgreSQL 9.6, pg_am contained many additional columns representing properties of index access methods. That data is now only directly visible at the C code level. However, `pg_index_column_has_property()` and related functions have been added to allow SQL queries to inspect index access method properties; see [System Catalog Information Functions](braised:ref/functions-info#system-catalog-information-functions).
:::
