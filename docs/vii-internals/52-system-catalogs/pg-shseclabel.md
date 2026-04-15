---
title: "52.50. pg_shseclabel"
id: catalog-pg-shseclabel
---

## pg_shseclabel

The catalog pg_shseclabel stores security labels on shared database objects.
Security labels can be manipulated with the [`SECURITY LABEL`](#sql-security-label) command.
For an easier way to view security labels, see [pg_seclabels](braised:ref/view-pg-seclabels).

See also [pg_seclabel](#catalog-pg-seclabel), which performs a similar function for security labels involving objects within a single database.

Unlike most system catalogs, pg_shseclabel is shared across all databases of a cluster: there is only one copy of pg_shseclabel per cluster, not one per database.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   objoid `oid` (references any OID column)

   The OID of the object this security label pertains to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   classoid `oid` (references [pg_class](#catalog-pg-class).oid)

   The OID of the system catalog this object appears in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   provider `text`

   The label provider associated with this label.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   label `text`

   The security label applied to this object.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_shseclabel Columns
