---
title: "52.42. pg_publication_rel"
id: catalog-pg-publication-rel
---

## pg_publication_rel

The catalog pg_publication_rel contains the mapping between relations and publications in the database.
This is a many-to-many mapping.
See also [pg_publication_tables](braised:ref/view-pg-publication-tables) for a more user-friendly view of this information.

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
   prpubid `oid` (references [pg_publication](#catalog-pg-publication).oid)

   Reference to publication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prrelid `oid` (references [pg_class](#catalog-pg-class).oid)

   Reference to relation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prqual `pg_node_tree`

   Expression tree (in `nodeToString()` representation) for the relation\'s publication qualifying condition. Null if there is no publication qualifying condition.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prattrs `int2vector` (references [pg_attribute](#catalog-pg-attribute).attnum)

   This is an array of values that indicates which table columns are part of the publication. For example, a value of `1 3` would mean that the first and the third table columns are published. A null value indicates that all columns are published.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_publication_rel Columns
