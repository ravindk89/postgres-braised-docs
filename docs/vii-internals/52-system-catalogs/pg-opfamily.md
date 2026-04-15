---
title: "52.35. pg_opfamily"
id: catalog-pg-opfamily
---

## pg_opfamily

The catalog pg_opfamily defines operator families.
Each operator family is a collection of operators and associated support routines that implement the semantics specified for a particular index access method.
Furthermore, the operators in a family are all "compatible", in a way that is specified by the access method.
The operator family concept allows cross-data-type operators to be used with indexes and to be reasoned about using knowledge of access method semantics.

Operator families are described at length in [Interfacing Extensions to Indexes](braised:ref/xindex).

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
   opfmethod `oid` (references [pg_am](#catalog-pg-am).oid)

   Index access method operator family is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opfname `name`

   Name of this operator family
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opfnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   Namespace of this operator family
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opfowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the operator family
  :::{/cell}
  :::{/row}
:::{/table}

: pg_opfamily Columns

The majority of the information defining an operator family is not in its pg_opfamily row, but in the associated rows in [pg_amop](#catalog-pg-amop), [pg_amproc](#catalog-pg-amproc), and [pg_opclass](#catalog-pg-opclass).
