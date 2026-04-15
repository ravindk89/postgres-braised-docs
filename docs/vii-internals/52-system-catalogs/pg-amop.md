---
title: "52.4. pg_amop"
id: catalog-pg-amop
---

## pg_amop

The catalog pg_amop stores information about operators associated with access method operator families.
There is one row for each operator that is a member of an operator family.
A family member can be either a search operator or an ordering operator.
An operator can appear in more than one family, but cannot appear in more than one search position nor more than one ordering position within a family. (It is allowed, though unlikely, for an operator to be used for both search and ordering purposes.)

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
   amopfamily `oid` (references [pg_opfamily](#catalog-pg-opfamily).oid)

   The operator family this entry is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amoplefttype `oid` (references [pg_type](#catalog-pg-type).oid)

   Left-hand input data type of operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amoprighttype `oid` (references [pg_type](#catalog-pg-type).oid)

   Right-hand input data type of operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amopstrategy `int2`

   Operator strategy number
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amoppurpose `char`

   Operator purpose, either `s` for search or `o` for ordering
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amopopr `oid` (references [pg_operator](#catalog-pg-operator).oid)

   OID of the operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amopmethod `oid` (references [pg_am](#catalog-pg-am).oid)

   Index access method operator family is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amopsortfamily `oid` (references [pg_opfamily](#catalog-pg-opfamily).oid)

   The B-tree operator family this entry sorts according to, if an ordering operator; zero if a search operator
  :::{/cell}
  :::{/row}
:::{/table}

: pg_amop Columns

A "search" operator entry indicates that an index of this operator family can be searched to find all rows satisfying `WHERE` *indexed_column* *operator* *constant*. Obviously, such an operator must return `boolean`, and its left-hand input type must match the index\'s column data type.

An "ordering" operator entry indicates that an index of this operator family can be scanned to return rows in the order represented by `ORDER BY` *indexed_column* *operator* *constant*. Such an operator could return any sortable data type, though again its left-hand input type must match the index\'s column data type. The exact semantics of the `ORDER BY` are specified by the amopsortfamily column, which must reference a B-tree operator family for the operator\'s result type.

:::{.callout type="note"}
At present, it\'s assumed that the sort order for an ordering operator is the default for the referenced operator family, i.e., `ASC NULLS LAST`. This might someday be relaxed by adding additional columns to specify sort options explicitly.
:::

An entry\'s amopmethod must match the opfmethod of its containing operator family (including amopmethod here is an intentional denormalization of the catalog structure for performance reasons).
Also, amoplefttype and amoprighttype must match the oprleft and oprright fields of the referenced [pg_operator](#catalog-pg-operator) entry.
