---
title: "53.9. pg_group"
id: view-pg-group
---

## pg_group

The view pg_group exists for backwards compatibility: it emulates a catalog that existed in PostgreSQL before version 8.1.
It shows the names and members of all roles that are marked as not rolcanlogin, which is an approximation to the set of roles that are being used as groups.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   groname `name` (references [pg_authid](#catalog-pg-authid).rolname)

   Name of the group
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grosysid `oid` (references [pg_authid](#catalog-pg-authid).oid)

   ID of this group
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   grolist `oid[]` (references [pg_authid](#catalog-pg-authid).oid)

   An array containing the IDs of the roles in this group
  :::{/cell}
  :::{/row}
:::{/table}

: pg_group Columns
