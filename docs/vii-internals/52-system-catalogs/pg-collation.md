---
title: "52.12. pg_collation"
id: catalog-pg-collation
---

## pg_collation

The catalog pg_collation describes the available collations, which are essentially mappings from an SQL name to operating system locale categories.
See [Collation Support](braised:ref/collation) for more information.

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
   collname `name`

   Collation name (unique per namespace and encoding)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this collation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the collation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collprovider `char`

   Provider of the collation: `d` = database default, `b` = builtin, `c` = libc, `i` = icu
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collisdeterministic `bool`

   Is the collation deterministic?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collencoding `int4`

   Encoding in which the collation is applicable, or -1 if it works for any encoding
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collcollate `text`

   `LC_COLLATE` for this collation object. If the provider is not `libc`, collcollate is `NULL` and colllocale is used instead.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collctype `text`

   `LC_CTYPE` for this collation object. If the provider is not `libc`, collctype is `NULL` and colllocale is used instead.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   colllocale `text`

   Collation provider locale name for this collation object. If the provider is `libc`, colllocale is `NULL`; collcollate and collctype are used instead.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collicurules `text`

   ICU collation rules for this collation object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   collversion `text`

   Provider-specific version of the collation. This is recorded when the collation is created and then checked when it is used, to detect changes in the collation definition that could lead to data corruption.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_collation Columns

Note that the unique key on this catalog is (collname, collencoding, collnamespace) not just (collname, collnamespace). PostgreSQL generally ignores all collations that do not have collencoding equal to either the current database\'s encoding or -1, and creation of new entries with the same name as an entry with collencoding = -1 is forbidden. Therefore it is sufficient to use a qualified SQL name (*schema*.*name*) to identify a collation, even though this is not unique according to the catalog definition. The reason for defining the catalog this way is that initdb fills it in at cluster initialization time with entries for all locales available on the system, so it must be able to hold entries for all encodings that might ever be used in the cluster.

In the `template0` database, it could be useful to create collations whose encoding does not match the database encoding, since they could match the encodings of databases later cloned from `template0`. This would currently have to be done manually.
