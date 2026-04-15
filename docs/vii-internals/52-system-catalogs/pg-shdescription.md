---
title: "52.49. pg_shdescription"
id: catalog-pg-shdescription
---

## pg_shdescription

The catalog pg_shdescription stores optional descriptions (comments) for shared database objects.
Descriptions can be manipulated with the [`COMMENT`](#sql-comment) command and viewed with psql\'s `\d` commands.

See also [pg_description](#catalog-pg-description), which performs a similar function for descriptions involving objects within a single database.

Unlike most system catalogs, pg_shdescription is shared across all databases of a cluster: there is only one copy of pg_shdescription per cluster, not one per database.

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

   The OID of the object this description pertains to
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
   description `text`

   Arbitrary text that serves as the description of this object
  :::{/cell}
  :::{/row}
:::{/table}

: pg_shdescription Columns
