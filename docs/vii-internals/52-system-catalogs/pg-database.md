---
title: "52.15. pg_database"
id: catalog-pg-database
---

## pg_database

The catalog pg_database stores information about the available databases.
Databases are created with the [`CREATE DATABASE`](#sql-createdatabase) command.
Consult [Managing Databases](#managing-databases) for details about the meaning of some of the parameters.

Unlike most system catalogs, pg_database is shared across all databases of a cluster: there is only one copy of pg_database per cluster, not one per database.

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
   datname `name`

   Database name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datdba `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the database, usually the user who created it
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   encoding `int4`

   Character encoding for this database ([`pg_encoding_to_char()`](#pg-encoding-to-char) can translate this number to the encoding name)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datlocprovider `char`

   Locale provider for this database: `b` = builtin, `c` = libc, `i` = icu
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datistemplate `bool`

   If true, then this database can be cloned by any user with `CREATEDB` privileges; if false, then only superusers or the owner of the database can clone it.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datallowconn `bool`

   If false then no one can connect to this database. This is used to protect the `template0` database from being altered.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dathasloginevt `bool`

   Indicates that there are login event triggers defined for this database. This flag is used to avoid extra lookups on the pg_event_trigger table during each backend startup. This flag is used internally by PostgreSQL and should not be manually altered or read for monitoring purposes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datconnlimit `int4`

   Sets maximum number of concurrent connections that can be made to this database. -1 means no limit, -2 indicates the database is invalid.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datfrozenxid `xid`

   All transaction IDs before this one have been replaced with a permanent ("frozen") transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent transaction ID wraparound or to allow `pg_xact` to be shrunk. It is the minimum of the per-table [pg_class](#catalog-pg-class).relfrozenxid values.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datminmxid `xid`

   All multixact IDs before this one have been replaced with a transaction ID in this database. This is used to track whether the database needs to be vacuumed in order to prevent multixact ID wraparound or to allow `pg_multixact` to be shrunk. It is the minimum of the per-table [pg_class](#catalog-pg-class).relminmxid values.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   dattablespace `oid` (references [pg_tablespace](#catalog-pg-tablespace).oid)

   The default tablespace for the database. Within this database, all tables for which [pg_class](#catalog-pg-class).reltablespace is zero will be stored in this tablespace; in particular, all the non-shared system catalogs will be there.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datcollate `text`

   LC_COLLATE for this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datctype `text`

   LC_CTYPE for this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datlocale `text`

   Collation provider locale name for this database. If the provider is `libc`, datlocale is `NULL`; datcollate and datctype are used instead.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   daticurules `text`

   ICU collation rules for this database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datcollversion `text`

   Provider-specific version of the collation. This is recorded when the database is created and then checked when it is used, to detect changes in the collation definition that could lead to data corruption.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_database Columns
