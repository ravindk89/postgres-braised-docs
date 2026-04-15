---
title: "52.26. pg_index"
id: catalog-pg-index
---

## pg_index

The catalog pg_index contains part of the information about indexes.
The rest is mostly in [pg_class](#catalog-pg-class).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for the table this index is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indnatts `int2`

   The total number of columns in the index (duplicates `pg_class.relnatts`); this number includes both key and included attributes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indnkeyatts `int2`

   The number of key columns in the index, not counting any included columns, which are merely stored and do not participate in the index semantics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisunique `bool`

   If true, this is a unique index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indnullsnotdistinct `bool`

   This value is only used for unique indexes. If false, this unique index will consider null values distinct (so the index can contain multiple null values in a column, the default PostgreSQL behavior). If it is true, it will consider null values to be equal (so the index can only contain one null value in a column).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisprimary `bool`

   If true, this index represents the primary key of the table (indisunique should always be true when this is true)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisexclusion `bool`

   If true, this index supports an exclusion constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indimmediate `bool`

   If true, the uniqueness check is enforced immediately on insertion (irrelevant if indisunique is not true)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisclustered `bool`

   If true, the table was last clustered on this index
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisvalid `bool`

   If true, the index is currently valid for queries. False means the index is possibly incomplete: it must still be modified by [`INSERT`](#sql-insert)/[`UPDATE`](#sql-update) operations, but it cannot safely be used for queries. If it is unique, the uniqueness property is not guaranteed true either.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indcheckxmin `bool`

   If true, queries must not use the index until the xmin of this pg_index row is below their `TransactionXmin` event horizon, because the table may contain broken [HOT chains](#storage-hot) with incompatible rows that they can see
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisready `bool`

   If true, the index is currently ready for inserts. False means the index must be ignored by [`INSERT`](#sql-insert)/[`UPDATE`](#sql-update) operations.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indislive `bool`

   If false, the index is in process of being dropped, and should be ignored for all purposes (including HOT-safety decisions)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indisreplident `bool`

   If true this index has been chosen as "replica identity" using [`ALTER TABLE ... REPLICA IDENTITY USING INDEX ...`](#sql-altertable-replica-identity)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indkey `int2vector` (references [pg_attribute](#catalog-pg-attribute).attnum)

   This is an array of indnatts values that indicate which table columns this index indexes. For example, a value of `1 3` would mean that the first and the third table columns make up the index entries. Key columns come before non-key (included) columns. A zero in this array indicates that the corresponding index attribute is an expression over the table columns, rather than a simple column reference.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indcollation `oidvector` (references [pg_collation](#catalog-pg-collation).oid)

   For each column in the index key (indnkeyatts values), this contains the OID of the collation to use for the index, or zero if the column is not of a collatable data type.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indclass `oidvector` (references [pg_opclass](#catalog-pg-opclass).oid)

   For each column in the index key (indnkeyatts values), this contains the OID of the operator class to use. See [pg_opclass](#catalog-pg-opclass) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indoption `int2vector`

   This is an array of indnkeyatts values that store per-column flag bits. The meaning of the bits is defined by the index\'s access method.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indexprs `pg_node_tree`

   Expression trees (in `nodeToString()` representation) for index attributes that are not simple column references. This is a list with one element for each zero entry in indkey. Null if all index attributes are simple references.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   indpred `pg_node_tree`

   Expression tree (in `nodeToString()` representation) for partial index predicate. Null if not a partial index.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_index Columns
