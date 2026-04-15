---
title: "52.38. pg_policy"
id: catalog-pg-policy
---

## pg_policy

The catalog pg_policy stores row-level security policies for tables.
A policy includes the kind of command that it applies to (possibly all commands), the roles that it applies to, the expression to be added as a security-barrier qualification to queries that include the table, and the expression to be added as a `WITH CHECK` option for queries that attempt to add new records to the table.

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
   polname `name`

   The name of the policy
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   The table to which the policy applies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polcmd `char`

   The command type to which the policy is applied: `r` for [SELECT](braised:ref/sql-select), `a` for [INSERT](braised:ref/sql-insert), `w` for [UPDATE](braised:ref/sql-update), `d` for [DELETE](braised:ref/sql-delete), or `*` for all
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polpermissive `bool`

   Is the policy permissive or restrictive?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polroles `oid[]` (references [pg_authid](#catalog-pg-authid).oid)

   The roles to which the policy is applied; zero means `PUBLIC` (and normally appears alone in the array)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polqual `pg_node_tree`

   The expression tree to be added to the security barrier qualifications for queries that use the table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   polwithcheck `pg_node_tree`

   The expression tree to be added to the WITH CHECK qualifications for queries that attempt to add rows to the table
  :::{/cell}
  :::{/row}
:::{/table}

: pg_policy Columns

:::{.callout type="note"}
Policies stored in pg_policy are applied only when [pg_class](#catalog-pg-class).relrowsecurity is set for their table.
:::
