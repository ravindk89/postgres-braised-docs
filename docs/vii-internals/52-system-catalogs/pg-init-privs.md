---
title: "52.28. pg_init_privs"
id: catalog-pg-init-privs
---

## pg_init_privs

The catalog pg_init_privs records information about the initial privileges of objects in the system.
There is one entry for each object in the database which has a non-default (non-NULL) initial set of privileges.

Objects can have initial privileges either by having those privileges set when the system is initialized (by initdb) or when the object is created during a [`CREATE EXTENSION`](#sql-createextension) and the extension script sets initial privileges using the [`GRANT`](#sql-grant) system.
Note that the system will automatically handle recording of the privileges during the extension script and that extension authors need only use the `GRANT` and `REVOKE` statements in their script to have the privileges recorded.
The `privtype` column indicates if the initial privilege was set by initdb or during a `CREATE EXTENSION` command.

Objects which have initial privileges set by initdb will have entries where `privtype` is `'i'`, while objects which have initial privileges set by `CREATE EXTENSION` will have entries where `privtype` is `'e'`.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objoid `oid` (references any OID column)

   The OID of the specific object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   classoid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the system catalog the object is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objsubid `int4`

   For a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   privtype `char`

   A code defining the type of initial privilege of this object; see text
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   initprivs `aclitem[]`

   The initial access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_init_privs Columns
