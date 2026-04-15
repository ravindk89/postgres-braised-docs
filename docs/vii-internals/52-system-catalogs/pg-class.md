---
title: "52.11. pg_class"
id: catalog-pg-class
---

## pg_class

The catalog pg_class describes tables and other objects that have columns or are otherwise similar to a table.
This includes indexes (but see also [pg_index](#catalog-pg-index)), sequences (but see also [pg_sequence](#catalog-pg-sequence)), views, materialized views, composite types, and TOAST tables; see relkind.
Below, when we mean all of these kinds of objects we speak of "relations".
Not all of pg_class\'s columns are meaningful for all relation kinds.

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
   relname `name`

   Name of the table, index, view, etc.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reltype `oid` (references [pg_type](#catalog-pg-type).oid)

   The OID of the data type that corresponds to this table\'s row type, if any; zero for indexes, sequences, and toast tables, which have no pg_type entry
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reloftype `oid` (references [pg_type](#catalog-pg-type).oid)

   For typed tables, the OID of the underlying composite type; zero for all other relations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relam `oid` (references [pg_am](#catalog-pg-am).oid)

   The access method used to access this table or index. Not meaningful if the relation is a sequence or has no on-disk file, except for partitioned tables, where, if set, it takes precedence over `default_table_access_method` when determining the access method to use for partitions created when one is not specified in the creation command.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relfilenode `oid`

   Name of the on-disk file of this relation; zero means this is a "mapped" relation whose disk file name is determined by low-level state
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reltablespace `oid` (references [pg_tablespace](#catalog-pg-tablespace).oid)

   The tablespace in which this relation is stored. If zero, the database\'s default tablespace is implied. Not meaningful if the relation has no on-disk file, except for partitioned tables, where this is the tablespace in which partitions will be created when one is not specified in the creation command.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relpages `int4`

   Size of the on-disk representation of this table in pages (of size `BLCKSZ`). This is only an estimate used by the planner. It is updated by [`VACUUM`](#sql-vacuum), [`ANALYZE`](#sql-analyze), and a few DDL commands such as [`CREATE INDEX`](#sql-createindex).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reltuples `float4`

   Number of live rows in the table. This is only an estimate used by the planner. It is updated by [`VACUUM`](#sql-vacuum), [`ANALYZE`](#sql-analyze), and a few DDL commands such as [`CREATE INDEX`](#sql-createindex). If the table has never yet been vacuumed or analyzed, reltuples contains `-1` indicating that the row count is unknown.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relallvisible `int4`

   Number of pages that are marked all-visible in the table\'s visibility map. This is only an estimate used by the planner. It is updated by [`VACUUM`](#sql-vacuum), [`ANALYZE`](#sql-analyze), and a few DDL commands such as [`CREATE INDEX`](#sql-createindex).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relallfrozen `int4`

   Number of pages that are marked all-frozen in the table\'s visibility map. This is only an estimate used for triggering autovacuums. It can also be used along with relallvisible for scheduling manual vacuums and tuning [vacuum\'s freezing behavior](braised:ref/runtime-config-vacuum). It is updated by [`VACUUM`](#sql-vacuum), [`ANALYZE`](#sql-analyze), and a few DDL commands such as [`CREATE INDEX`](#sql-createindex).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reltoastrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   OID of the TOAST table associated with this table, zero if none. The TOAST table stores large attributes "out of line" in a secondary table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relhasindex `bool`

   True if this is a table and it has (or recently had) any indexes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relisshared `bool`

   True if this table is shared across all databases in the cluster. Only certain system catalogs (such as [pg_database](#catalog-pg-database)) are shared.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relpersistence `char`

   `p` = permanent table/sequence, `u` = unlogged table/sequence, `t` = temporary table/sequence
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relkind `char`

   `r` = ordinary table, `i` = index, `S` = sequence, `t` = TOAST table, `v` = view, `m` = materialized view, `c` = composite type, `f` = foreign table, `p` = partitioned table, `I` = partitioned index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relnatts `int2`

   Number of user columns in the relation (system columns not counted). There must be this many corresponding entries in [pg_attribute](#catalog-pg-attribute). See also pg_attribute.attnum.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relchecks `int2`

   Number of `CHECK` constraints on the table; see [pg_constraint](#catalog-pg-constraint) catalog
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relhasrules `bool`

   True if table has (or once had) rules; see [pg_rewrite](#catalog-pg-rewrite) catalog
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relhastriggers `bool`

   True if table has (or once had) triggers; see [pg_trigger](#catalog-pg-trigger) catalog
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relhassubclass `bool`

   True if table or index has (or once had) any inheritance children or partitions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relrowsecurity `bool`

   True if table has row-level security enabled; see [pg_policy](#catalog-pg-policy) catalog
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relforcerowsecurity `bool`

   True if row-level security (when enabled) will also apply to table owner; see [pg_policy](#catalog-pg-policy) catalog
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relispopulated `bool`

   True if relation is populated (this is true for all relations other than some materialized views)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relreplident `char`

   Columns used to form "replica identity" for rows: `d` = default (primary key, if any), `n` = nothing, `f` = all columns, `i` = index with indisreplident set (same as nothing if the index used has been dropped)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relispartition `bool`

   True if table or index is a partition
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relrewrite `oid` (references [pg_class](#catalog-pg-class).oid)

   For new relations being written during a DDL operation that requires a table rewrite, this contains the OID of the original relation; otherwise zero. That state is only visible internally; this field should never contain anything other than zero for a user-visible relation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relfrozenxid `xid`

   All transaction IDs before this one have been replaced with a permanent ("frozen") transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent transaction ID wraparound or to allow `pg_xact` to be shrunk. Zero (`InvalidTransactionId`) if the relation is not a table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relminmxid `xid`

   All multixact IDs before this one have been replaced by a transaction ID in this table. This is used to track whether the table needs to be vacuumed in order to prevent multixact ID wraparound or to allow `pg_multixact` to be shrunk. Zero (`InvalidMultiXactId`) if the relation is not a table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   reloptions `text[]`

   Access-method-specific options, as "keyword=value" strings
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   relpartbound `pg_node_tree`

   If table is a partition (see relispartition), internal representation of the partition bound
  :::{/cell}
  :::{/row}
:::{/table}

: pg_class Columns

Several of the Boolean flags in pg_class are maintained lazily: they are guaranteed to be true if that\'s the correct state, but may not be reset to false immediately when the condition is no longer true. For example, relhasindex is set by [`CREATE INDEX`](#sql-createindex), but it is never cleared by [`DROP INDEX`](#sql-dropindex). Instead, [`VACUUM`](#sql-vacuum) clears relhasindex if it finds the table has no indexes. This arrangement avoids race conditions and improves concurrency.
