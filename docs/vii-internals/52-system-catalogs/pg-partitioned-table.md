---
title: "52.37. pg_partitioned_table"
id: catalog-pg-partitioned-table
---

## pg_partitioned_table

The catalog pg_partitioned_table stores information about how tables are partitioned.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for this partitioned table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partstrat `char`

   Partitioning strategy; `h` = hash partitioned table, `l` = list partitioned table, `r` = range partitioned table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partnatts `int2`

   The number of columns in the partition key
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partdefid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the [pg_class](#catalog-pg-class) entry for the default partition of this partitioned table, or zero if this partitioned table does not have a default partition
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partattrs `int2vector` (references [pg_attribute](#catalog-pg-attribute).attnum)

   This is an array of partnatts values that indicate which table columns are part of the partition key. For example, a value of `1 3` would mean that the first and the third table columns make up the partition key. A zero in this array indicates that the corresponding partition key column is an expression, rather than a simple column reference.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partclass `oidvector` (references [pg_opclass](#catalog-pg-opclass).oid)

   For each column in the partition key, this contains the OID of the operator class to use. See [pg_opclass](#catalog-pg-opclass) for details.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partcollation `oidvector` (references [pg_collation](#catalog-pg-collation).oid)

   For each column in the partition key, this contains the OID of the collation to use for partitioning, or zero if the column is not of a collatable data type.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   partexprs `pg_node_tree`

   Expression trees (in `nodeToString()` representation) for partition key columns that are not simple column references. This is a list with one element for each zero entry in partattrs. Null if all partition key columns are simple references.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_partitioned_table Columns
