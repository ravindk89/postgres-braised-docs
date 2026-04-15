---
title: "53.18. pg_publication_tables"
id: view-pg-publication-tables
---

## pg_publication_tables

The view pg_publication_tables provides information about the mapping between publications and information of tables they contain.
Unlike the underlying catalog [pg_publication_rel](#catalog-pg-publication-rel), this view expands publications defined as [`FOR ALL TABLES`](#sql-createpublication-params-for-all-tables) and [`FOR TABLES IN SCHEMA`](#sql-createpublication-params-for-tables-in-schema), so for such publications there will be a row for each eligible table.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pubname `name` (references [pg_publication](#catalog-pg-publication).pubname)

   Name of publication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   schemaname `name` (references [pg_namespace](#catalog-pg-namespace).nspname)

   Name of schema containing table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   tablename `name` (references [pg_class](#catalog-pg-class).relname)

   Name of table
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   attnames `name[]` (references [pg_attribute](#catalog-pg-attribute).attname)

   Names of table columns included in the publication. This contains all the columns of the table when the user didn\'t specify the column list for the table.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rowfilter `text`

   Expression for the table\'s publication qualifying condition
  :::{/cell}
  :::{/row}
:::{/table}

: pg_publication_tables Columns
