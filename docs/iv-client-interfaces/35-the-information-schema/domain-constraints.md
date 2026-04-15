---
title: "35.21. domain_constraints"
id: infoschema-domain-constraints
---

## `domain_constraints`

The view `domain_constraints` contains all constraints belonging to domains defined in the current database.
Only those domains are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_catalog `sql_identifier`

   Name of the database that contains the constraint (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_schema `sql_identifier`

   Name of the schema that contains the constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   constraint_name `sql_identifier`

   Name of the constraint
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_catalog `sql_identifier`

   Name of the database that contains the domain (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_schema `sql_identifier`

   Name of the schema that contains the domain
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   domain_name `sql_identifier`

   Name of the domain
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_deferrable `yes_or_no`

   `YES` if the constraint is deferrable, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   initially_deferred `yes_or_no`

   `YES` if the constraint is deferrable and initially deferred, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: domain_constraints Columns
