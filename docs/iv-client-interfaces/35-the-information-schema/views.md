---
title: "35.66. views"
id: infoschema-views
---

## `views`

The view `views` contains all views defined in the current database.
Only those views are shown that the current user has access to (by way of being the owner or having some privilege).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_catalog `sql_identifier`

   Name of the database that contains the view (always the current database)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_schema `sql_identifier`

   Name of the schema that contains the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   table_name `sql_identifier`

   Name of the view
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   view_definition `character_data`

   Query expression defining the view (null if the view is not owned by a currently enabled role)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   check_option `character_data`

   `CASCADED` or `LOCAL` if the view has a `CHECK OPTION` defined on it, `NONE` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_updatable `yes_or_no`

   `YES` if the view is updatable (allows `UPDATE` and `DELETE`), `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_insertable_into `yes_or_no`

   `YES` if the view is insertable into (allows `INSERT`), `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_trigger_updatable `yes_or_no`

   `YES` if the view has an `INSTEAD OF` `UPDATE` trigger defined on it, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_trigger_deletable `yes_or_no`

   `YES` if the view has an `INSTEAD OF` `DELETE` trigger defined on it, `NO` if not
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_trigger_insertable_into `yes_or_no`

   `YES` if the view has an `INSTEAD OF` `INSERT` trigger defined on it, `NO` if not
  :::{/cell}
  :::{/row}
:::{/table}

: views Columns
