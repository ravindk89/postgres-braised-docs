---
title: "52.34. pg_operator"
id: catalog-pg-operator
---

## pg_operator

The catalog pg_operator stores information about operators.
See [CREATE OPERATOR](braised:ref/sql-createoperator) and [User-Defined Operators](braised:ref/xoper) for more information.

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
   oprname `name`

   Name of the operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprkind `char`

   `b` = infix operator ("both"), or `l` = prefix operator ("left")
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprcanmerge `bool`

   This operator supports merge joins
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprcanhash `bool`

   This operator supports hash joins
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprleft `oid` (references [pg_type](#catalog-pg-type).oid)

   Type of the left operand (zero for a prefix operator)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprright `oid` (references [pg_type](#catalog-pg-type).oid)

   Type of the right operand
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprresult `oid` (references [pg_type](#catalog-pg-type).oid)

   Type of the result (zero for a not-yet-defined "shell" operator)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprcom `oid` (references [pg_operator](#catalog-pg-operator).oid)

   Commutator of this operator (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprnegate `oid` (references [pg_operator](#catalog-pg-operator).oid)

   Negator of this operator (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprcode `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Function that implements this operator (zero for a not-yet-defined "shell" operator)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprrest `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Restriction selectivity estimation function for this operator (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oprjoin `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Join selectivity estimation function for this operator (zero if none)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_operator Columns
