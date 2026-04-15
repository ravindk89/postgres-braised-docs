---
title: "52.13. pg_constraint"
id: catalog-pg-constraint
---

## pg_constraint

The catalog pg_constraint stores check, not-null, primary key, unique, foreign key, and exclusion constraints on tables. (Column constraints are not treated specially.
Every column constraint is equivalent to some table constraint.)

User-defined constraint triggers (created with [`CREATE CONSTRAINT TRIGGER`](#sql-createtrigger)) also give rise to an entry in this table.

Check constraints on domains are stored here, too.

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
   conname `name`

   Constraint name (not necessarily unique!)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   connamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   contype `char`

   `c` = check constraint, `f` = foreign key constraint, `n` = not-null constraint, `p` = primary key constraint, `u` = unique constraint, `t` = constraint trigger, `x` = exclusion constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   condeferrable `bool`

   Is the constraint deferrable?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   condeferred `bool`

   Is the constraint deferred by default?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conenforced `bool`

   Is the constraint enforced?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   convalidated `bool`

   Has the constraint been validated?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The table this constraint is on; zero if not a table constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   contypid `oid` (references [pg_type](#catalog-pg-type).oid)

   The domain this constraint is on; zero if not a domain constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conindid `oid` (references [pg_class](#catalog-pg-class).oid)

   The index supporting this constraint, if it\'s a unique, primary key, foreign key, or exclusion constraint; else zero
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conparentid `oid` (references [pg_constraint](#catalog-pg-constraint).oid)

   The corresponding constraint of the parent partitioned table, if this is a constraint on a partition; else zero
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   If a foreign key, the referenced table; else zero
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confupdtype `char`

   Foreign key update action code: `a` = no action, `r` = restrict, `c` = cascade, `n` = set null, `d` = set default
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confdeltype `char`

   Foreign key deletion action code: `a` = no action, `r` = restrict, `c` = cascade, `n` = set null, `d` = set default
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confmatchtype `char`

   Foreign key match type: `f` = full, `p` = partial, `s` = simple
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conislocal `bool`

   This constraint is defined locally for the relation. Note that a constraint can be locally defined and inherited simultaneously.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   coninhcount `int2`

   The number of direct inheritance ancestors this constraint has. A constraint with a nonzero number of ancestors cannot be dropped nor renamed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   connoinherit `bool`

   This constraint is defined locally for the relation. It is a non-inheritable constraint.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conperiod `bool`

   This constraint is defined with `WITHOUT OVERLAPS` (for primary keys and unique constraints) or `PERIOD` (for foreign keys).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conkey `int2[]` (references [pg_attribute](#catalog-pg-attribute).attnum)

   If a table constraint (including foreign keys, but not constraint triggers), list of the constrained columns
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confkey `int2[]` (references [pg_attribute](#catalog-pg-attribute).attnum)

   If a foreign key, list of the referenced columns
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conpfeqop `oid[]` (references [pg_operator](#catalog-pg-operator).oid)

   If a foreign key, list of the equality operators for PK = FK comparisons
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conppeqop `oid[]` (references [pg_operator](#catalog-pg-operator).oid)

   If a foreign key, list of the equality operators for PK = PK comparisons
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conffeqop `oid[]` (references [pg_operator](#catalog-pg-operator).oid)

   If a foreign key, list of the equality operators for FK = FK comparisons
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confdelsetcols `int2[]` (references [pg_attribute](#catalog-pg-attribute).attnum)

   If a foreign key with a `SET NULL` or `SET DEFAULT` delete action, the columns that will be updated. If null, all of the referencing columns will be updated.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conexclop `oid[]` (references [pg_operator](#catalog-pg-operator).oid)

   If an exclusion constraint or `WITHOUT OVERLAPS` primary key/unique constraint, list of the per-column exclusion operators.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conbin `pg_node_tree`

   If a check constraint, an internal representation of the expression. (It\'s recommended to use `pg_get_constraintdef()` to extract the definition of a check constraint.)
  :::{/cell}
  :::{/row}
:::{/table}

: pg_constraint Columns

In the case of an exclusion constraint, conkey is only useful for constraint elements that are simple column references. For other cases, a zero appears in conkey and the associated index must be consulted to discover the expression that is constrained. (conkey thus has the same contents as [pg_index](#catalog-pg-index).indkey for the index.)

:::{.callout type="note"}
`pg_class.relchecks` needs to agree with the number of check-constraint entries found in this table for each relation.
:::
