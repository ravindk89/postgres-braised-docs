---
title: "52.2. pg_aggregate"
id: catalog-pg-aggregate
---

## pg_aggregate

The catalog pg_aggregate stores information about aggregate functions.
An aggregate function is a function that operates on a set of values (typically one column from each row that matches a query condition) and returns a single value computed from all these values.
Typical aggregate functions are `sum`, `count`, and `max`.
Each entry in pg_aggregate is an extension of an entry in [pg_proc](#catalog-pg-proc).
The pg_proc entry carries the aggregate\'s name, input and output data types, and other information that is similar to ordinary functions.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggfnoid `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   pg_proc OID of the aggregate function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggkind `char`

   Aggregate kind: `n` for "normal" aggregates, `o` for "ordered-set" aggregates, or `h` for "hypothetical-set" aggregates
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggnumdirectargs `int2`

   Number of direct (non-aggregated) arguments of an ordered-set or hypothetical-set aggregate, counting a variadic array as one argument. If equal to pronargs, the aggregate must be variadic and the variadic array describes the aggregated arguments as well as the final direct arguments. Always zero for normal aggregates.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggtransfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Transition function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggfinalfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Final function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggcombinefn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Combine function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggserialfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Serialization function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggdeserialfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Deserialization function (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmtransfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Forward transition function for moving-aggregate mode (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggminvtransfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Inverse transition function for moving-aggregate mode (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmfinalfn `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Final function for moving-aggregate mode (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggfinalextra `bool`

   True to pass extra dummy arguments to aggfinalfn
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmfinalextra `bool`

   True to pass extra dummy arguments to aggmfinalfn
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggfinalmodify `char`

   Whether aggfinalfn modifies the transition state value: `r` if it is read-only, `s` if the aggtransfn cannot be applied after the aggfinalfn, or `w` if it writes on the value
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmfinalmodify `char`

   Like aggfinalmodify, but for the aggmfinalfn
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggsortop `oid` (references [pg_operator](#catalog-pg-operator).oid)

   Associated sort operator (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggtranstype `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type of the aggregate function\'s internal transition (state) data
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggtransspace `int4`

   Approximate average size (in bytes) of the transition state data, or zero to use a default estimate
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmtranstype `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type of the aggregate function\'s internal transition (state) data for moving-aggregate mode (zero if none)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggmtransspace `int4`

   Approximate average size (in bytes) of the transition state data for moving-aggregate mode, or zero to use a default estimate
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   agginitval `text`

   The initial value of the transition state. This is a text field containing the initial value in its external string representation. If this field is null, the transition state value starts out null.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   aggminitval `text`

   The initial value of the transition state for moving-aggregate mode. This is a text field containing the initial value in its external string representation. If this field is null, the transition state value starts out null.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_aggregate Columns

New aggregate functions are registered with the [`CREATE AGGREGATE`](#sql-createaggregate) command. See [User-Defined Aggregates](braised:ref/xaggr) for more information about writing aggregate functions and the meaning of the transition functions, etc.
