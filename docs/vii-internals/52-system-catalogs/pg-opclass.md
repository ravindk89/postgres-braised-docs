---
title: "52.33. pg_opclass"
id: catalog-pg-opclass
---

## pg_opclass

The catalog pg_opclass defines index access method operator classes.
Each operator class defines semantics for index columns of a particular data type and a particular index access method.
An operator class essentially specifies that a particular operator family is applicable to a particular indexable column data type.
The set of operators from the family that are actually usable with the indexed column are whichever ones accept the column\'s data type as their left-hand input.

Operator classes are described at length in [Interfacing Extensions to Indexes](braised:ref/xindex).

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
   opcmethod `oid` (references [pg_am](#catalog-pg-am).oid)

   Index access method operator class is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcname `name`

   Name of this operator class
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   Namespace of this operator class
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the operator class
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcfamily `oid` (references [pg_opfamily](#catalog-pg-opfamily).oid)

   Operator family containing the operator class
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcintype `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type that the operator class indexes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opcdefault `bool`

   True if this operator class is the default for opcintype
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   opckeytype `oid` (references [pg_type](#catalog-pg-type).oid)

   Type of data stored in index, or zero if same as opcintype
  :::{/cell}
  :::{/row}
:::{/table}

: pg_opclass Columns

An operator class\'s opcmethod must match the opfmethod of its containing operator family. Also, there must be no more than one pg_opclass row having opcdefault true for any given combination of opcmethod and opcintype.
