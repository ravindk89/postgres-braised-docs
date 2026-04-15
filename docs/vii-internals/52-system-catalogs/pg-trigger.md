---
title: "52.58. pg_trigger"
id: catalog-pg-trigger
---

## pg_trigger

The catalog pg_trigger stores triggers on tables and views.
See [CREATE TRIGGER](braised:ref/sql-createtrigger) for more information.

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
   tgrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The table this trigger is on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgparentid `oid` (references [pg_trigger](#catalog-pg-trigger).oid)

   Parent trigger that this trigger is cloned from (this happens when partitions are created or attached to a partitioned table); zero if not a clone
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgname `name`

   Trigger name (must be unique among triggers of same table)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgfoid `oid` (references [pg_proc](#catalog-pg-proc).oid)

   The function to be called
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgtype `int2`

   Bit mask identifying trigger firing conditions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgenabled `char`

   Controls in which [session_replication_role (enum)
      
       session_replication_role configuration parameter](braised:ref/runtime-config-client#session-replication-role-enum-session-replication-role-configuration-parameter) modes the trigger fires. `O` = trigger fires in "origin" and "local" modes, `D` = trigger is disabled, `R` = trigger fires in "replica" mode, `A` = trigger fires always.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgisinternal `bool`

   True if trigger is internally generated (usually, to enforce the constraint identified by tgconstraint)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgconstrrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The table referenced by a referential integrity constraint (zero if trigger is not for a referential integrity constraint)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgconstrindid `oid` (references [pg_class](#catalog-pg-class).oid)

   The index supporting a unique, primary key, referential integrity, or exclusion constraint (zero if trigger is not for one of these types of constraint)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgconstraint `oid` (references [pg_constraint](#catalog-pg-constraint).oid)

   The [pg_constraint](#catalog-pg-constraint) entry associated with the trigger (zero if trigger is not for a constraint)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgdeferrable `bool`

   True if constraint trigger is deferrable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tginitdeferred `bool`

   True if constraint trigger is initially deferred
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgnargs `int2`

   Number of argument strings passed to trigger function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgattr `int2vector` (references [pg_attribute](#catalog-pg-attribute).attnum)

   Column numbers, if trigger is column-specific; otherwise an empty array
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgargs `bytea`

   Argument strings to pass to trigger, each NULL-terminated
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgqual `pg_node_tree`

   Expression tree (in `nodeToString()` representation) for the trigger\'s `WHEN` condition, or null if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgoldtable `name`

   `REFERENCING` clause name for `OLD TABLE`, or null if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tgnewtable `name`

   `REFERENCING` clause name for `NEW TABLE`, or null if none
  :::{/cell}
  :::{/row}
:::{/table}

: pg_trigger Columns

Currently, column-specific triggering is supported only for `UPDATE` events, and so tgattr is relevant only for that event type. tgtype might contain bits for other event types as well, but those are presumed to be table-wide regardless of what is in tgattr.

:::{.callout type="note"}
When tgconstraint is nonzero, tgconstrrelid, tgconstrindid, tgdeferrable, and tginitdeferred are largely redundant with the referenced [pg_constraint](#catalog-pg-constraint) entry. However, it is possible for a non-deferrable trigger to be associated with a deferrable constraint: foreign key constraints can have some deferrable and some non-deferrable triggers.
:::

:::{.callout type="note"}
`pg_class.relhastriggers` must be true if a relation has any triggers in this catalog.
:::
