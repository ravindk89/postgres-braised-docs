---
title: "53.15. pg_policies"
id: view-pg-policies
---

## pg_policies

The view pg_policies provides access to useful information about each row-level security policy in the database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name` (references [pg_namespace](#catalog-pg-namespace).nspname)

   Name of schema containing table policy is on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablename `name` (references [pg_class](#catalog-pg-class).relname)

   Name of table policy is on
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   policyname `name` (references [pg_policy](#catalog-pg-policy).polname)

   Name of policy
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   permissive `text`

   Is the policy permissive or restrictive?
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   roles `name[]`

   The roles to which this policy applies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cmd `text`

   The command type to which the policy is applied
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   qual `text`

   The expression added to the security barrier qualifications for queries that this policy applies to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   with_check `text`

   The expression added to the WITH CHECK qualifications for queries that attempt to add rows to this table
  :::{/cell}
  :::{/row}
:::{/table}

: pg_policies Columns
