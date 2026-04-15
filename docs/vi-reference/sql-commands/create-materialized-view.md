---
title: "CREATE MATERIALIZED VIEW"
layout: reference
id: sql-creatematerializedview
description: "define a new materialized view"
---

:::synopsis
CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
 [ (column_name [, ...] ) ]
 [ USING method ]
 [ WITH ( storage_parameter [= value] [, ... ] ) ]
 [ TABLESPACE tablespace_name ]
 AS query
 [ WITH [ NO ] DATA ]
:::

## Description

`CREATE MATERIALIZED VIEW` defines a materialized view of a query.
The query is executed and used to populate the view at the time the command is issued (unless `WITH NO DATA` is used) and may be refreshed later using `REFRESH MATERIALIZED VIEW`.

`CREATE MATERIALIZED VIEW` is similar to `CREATE TABLE AS`, except that it also remembers the query used to initialize the view, so that it can be refreshed later upon demand.
A materialized view has many of the same properties as a table, but there is no support for temporary materialized views.

`CREATE MATERIALIZED VIEW` requires `CREATE` privilege on the schema used for the materialized view.

## Parameters

:::{.dl}
:::{.item term="`IF NOT EXISTS`"}
Do not throw an error if a materialized view with the same name already exists. A notice is issued in this case. Note that there is no guarantee that the existing materialized view is anything like the one that would have been created.
:::{/item}
:::{.item term="*table_name*"}
The name (optionally schema-qualified) of the materialized view to be created. The name must be distinct from the name of any other relation (table, sequence, index, view, materialized view, or foreign table) in the same schema.
:::{/item}
:::{.item term="*column_name*"}
The name of a column in the new materialized view. If column names are not provided, they are taken from the output column names of the query.
:::{/item}
:::{.item term="`USING method`"}
This optional clause specifies the table access method to use to store the contents for the new materialized view; the method needs be an access method of type `TABLE`. See [Table Access Method Interface Definition](braised:ref/tableam) for more information. If this option is not specified, the default table access method is chosen for the new materialized view. See [default_table_access_method (string)
      
   default_table_access_method configuration parameter](braised:ref/runtime-config-client#default-table-access-method-string-default-table-access-method-configuration-parameter) for more information.
:::{/item}
:::{.item term="`WITH ( storage_parameter [= value] [, ... ] )`"}
This clause specifies optional storage parameters for the new materialized view; see [Storage Parameters](braised:ref/sql-createtable#storage-parameters) in the [CREATE TABLE](braised:ref/sql-createtable) documentation for more information. All parameters supported for `CREATE TABLE` are also supported for `CREATE MATERIALIZED VIEW`. See [CREATE TABLE](braised:ref/sql-createtable) for more information.
:::{/item}
:::{.item term="`TABLESPACE tablespace_name`"}
The *tablespace_name* is the name of the tablespace in which the new materialized view is to be created. If not specified, [default_tablespace (string)
      
   default_tablespace configuration parameter
      
  tablespacedefault](braised:ref/runtime-config-client#default-tablespace-string-default-tablespace-configuration-parameter-tablespacedefault) is consulted.
:::{/item}
:::{.item term="*query*"}
A [`SELECT`](#sql-select), `TABLE`, or [`VALUES`](#sql-values) command. This query will run within a security-restricted operation; in particular, calls to functions that themselves create temporary tables will fail. Also, while the query is running, the [search_path (string)
      
   search_path configuration parameter
      
  pathfor schemas](braised:ref/runtime-config-client#search-path-string-search-path-configuration-parameter-pathfor-schemas) is temporarily changed to `pg_catalog, pg_temp`.
:::{/item}
:::{.item term="`WITH [ NO ] DATA`"}
This clause specifies whether or not the materialized view should be populated at creation time. If not, the materialized view will be flagged as unscannable and cannot be queried until `REFRESH MATERIALIZED VIEW` is used.
:::{/item}
:::{/dl}

## Compatibility

`CREATE MATERIALIZED VIEW` is a PostgreSQL extension.
