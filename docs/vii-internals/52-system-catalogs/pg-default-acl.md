---
title: "52.17. pg_default_acl"
id: catalog-pg-default-acl
---

## pg_default_acl

The catalog pg_default_acl stores initial privileges to be assigned to newly created objects.

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
   defaclrole `oid` (references [pg_authid](#catalog-pg-authid).oid)

   The OID of the role associated with this entry
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   defaclnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace associated with this entry, or zero if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   defaclobjtype `char`

   Type of object this entry is for: `r` = relation (table, view), `S` = sequence, `f` = function, `T` = type, `n` = schema, `L` = large object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   defaclacl `aclitem[]`

   Access privileges that this type of object should have on creation
  :::{/cell}
  :::{/row}
:::{/table}

: pg_default_acl Columns

A pg_default_acl entry shows the initial privileges to be assigned to an object belonging to the indicated user. There are currently two types of entry: "global" entries with defaclnamespace = zero, and "per-schema" entries that reference a particular schema. If a global entry is present then it *overrides* the normal hard-wired default privileges for the object type. A per-schema entry, if present, represents privileges to be *added to* the global or hard-wired default privileges.

Note that when an ACL entry in another catalog is null, it is taken to represent the hard-wired default privileges for its object, *not* whatever might be in pg_default_acl at the moment. pg_default_acl is only consulted during object creation.
