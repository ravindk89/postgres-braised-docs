---
title: "52.19. pg_description"
id: catalog-pg-description
---

## pg_description

The catalog pg_description stores optional descriptions (comments) for each database object.
Descriptions can be manipulated with the [`COMMENT`](#sql-comment) command and viewed with psql\'s `\d` commands.
Descriptions of many built-in system objects are provided in the initial contents of pg_description.

See also [pg_shdescription](#catalog-pg-shdescription), which performs a similar function for descriptions involving objects that are shared across a database cluster.

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
   objsubid `int4`

   For a comment on a table column, this is the column number (the objoid and classoid refer to the table itself). For all other object types, this column is zero.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   description `text`

   Arbitrary text that serves as the description of this object
  :::{/cell}
  :::{/row}
:::{/table}

: pg_description Columns
