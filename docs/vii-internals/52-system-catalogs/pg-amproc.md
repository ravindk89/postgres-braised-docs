---
title: "52.5. pg_amproc"
id: catalog-pg-amproc
---

## pg_amproc

The catalog pg_amproc stores information about support functions associated with access method operator families.
There is one row for each support function belonging to an operator family.

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
   amprocfamily `oid` (references [pg_opfamily](#catalog-pg-opfamily).oid)

   The operator family this entry is for
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amproclefttype `oid` (references [pg_type](#catalog-pg-type).oid)

   Left-hand input data type of associated operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amprocrighttype `oid` (references [pg_type](#catalog-pg-type).oid)

   Right-hand input data type of associated operator
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amprocnum `int2`

   Support function number
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   amproc `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   OID of the function
  :::{/cell}
  :::{/row}
:::{/table}

: pg_amproc Columns

The usual interpretation of the amproclefttype and amprocrighttype fields is that they identify the left and right input types of the operator(s) that a particular support function supports. For some access methods these match the input data type(s) of the support function itself, for others not. There is a notion of "default" support functions for an index, which are those with amproclefttype and amprocrighttype both equal to the index operator class\'s opcintype.
