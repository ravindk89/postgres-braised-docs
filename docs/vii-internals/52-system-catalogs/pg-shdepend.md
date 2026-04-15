---
title: "52.48. pg_shdepend"
id: catalog-pg-shdepend
---

## pg_shdepend

The catalog pg_shdepend records the dependency relationships between database objects and shared objects, such as roles.
This information allows PostgreSQL to ensure that those objects are unreferenced before attempting to delete them.

See also [pg_depend](#catalog-pg-depend), which performs a similar function for dependencies involving objects within a single database.

Unlike most system catalogs, pg_shdepend is shared across all databases of a cluster: there is only one copy of pg_shdepend per cluster, not one per database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dbid `oid` (references [pg_database](#catalog-pg-database).oid)

   The OID of the database the dependent object is in, or zero for a shared object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   classid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the system catalog the dependent object is in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objid `oid` (references any OID column)

   The OID of the specific dependent object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objsubid `int4`

   For a table column, this is the column number (the objid and classid refer to the table itself). For all other object types, this column is zero.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   refclassid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the system catalog the referenced object is in (must be a shared catalog)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   refobjid `oid` (references any OID column)

   The OID of the specific referenced object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   deptype `char`

   A code defining the specific semantics of this dependency relationship; see text
  :::{/cell}
  :::{/row}
:::{/table}

: pg_shdepend Columns

In all cases, a pg_shdepend entry indicates that the referenced object cannot be dropped without also dropping the dependent object. However, there are several subflavors identified by deptype:

:::{.dl}
:::{.item term="`SHARED_DEPENDENCY_OWNER` (`o`)"}
The referenced object (which must be a role) is the owner of the dependent object.
:::{/item}
:::{.item term="`SHARED_DEPENDENCY_ACL` (`a`)"}
The referenced object (which must be a role) is mentioned in the ACL of the dependent object. (A `SHARED_DEPENDENCY_ACL` entry is not made for the owner of the object, since the owner will have a `SHARED_DEPENDENCY_OWNER` entry anyway.)
:::{/item}
:::{.item term="`SHARED_DEPENDENCY_INITACL` (`i`)"}
The referenced object (which must be a role) is mentioned in a [pg_init_privs](#catalog-pg-init-privs) entry for the dependent object.
:::{/item}
:::{.item term="`SHARED_DEPENDENCY_POLICY` (`r`)"}
The referenced object (which must be a role) is mentioned as the target of a dependent policy object.
:::{/item}
:::{.item term="`SHARED_DEPENDENCY_TABLESPACE` (`t`)"}
The referenced object (which must be a tablespace) is mentioned as the tablespace for a relation that doesn\'t have storage.
:::{/item}
:::{/dl}

Other dependency flavors might be needed in future. Note in particular that the current definition only supports roles and tablespaces as referenced objects.

As in the pg_depend catalog, most objects created during initdb are considered "pinned". No entries are made in pg_shdepend that would have a pinned object as either referenced or dependent object.
