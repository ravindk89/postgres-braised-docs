---
title: "52.40. pg_publication"
id: catalog-pg-publication
---

## pg_publication

The catalog pg_publication contains all publications created in the database.
For more on publications see [Publication](braised:ref/logical-replication-publication).

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
   pubname `name`

   Name of the publication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the publication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   puballtables `bool`

   If true, this publication automatically includes all tables in the database, including any that will be created in the future.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubinsert `bool`

   If true, [INSERT](braised:ref/sql-insert) operations are replicated for tables in the publication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubupdate `bool`

   If true, [UPDATE](braised:ref/sql-update) operations are replicated for tables in the publication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubdelete `bool`

   If true, [DELETE](braised:ref/sql-delete) operations are replicated for tables in the publication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubtruncate `bool`

   If true, [TRUNCATE](braised:ref/sql-truncate) operations are replicated for tables in the publication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubviaroot `bool`

   If true, operations on a leaf partition are replicated using the identity and schema of its topmost partitioned ancestor mentioned in the publication instead of its own.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubgencols `char`

   Controls how to handle generated column replication when there is no publication column list: `n` = generated columns in the tables associated with the publication should not be replicated, `s` = stored generated columns in the tables associated with the publication should be replicated.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_publication Columns
