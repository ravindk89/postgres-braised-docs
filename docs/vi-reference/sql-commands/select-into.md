---
title: "SELECT INTO"
layout: reference
id: sql-selectinto
description: "define a new table from the results of a query"
---

:::synopsis
[ WITH [ RECURSIVE ] with_query [, ...] ]
SELECT [ ALL | DISTINCT [ ON ( expression [, ...] ) ] ]
 [ { * | expression [ [ AS ] output_name ] } [, ...] ]
 INTO [ TEMPORARY | TEMP | UNLOGGED ] [ TABLE ] new_table
 [ FROM from_item [, ...] ]
 [ WHERE condition ]
 [ GROUP BY expression [, ...] ]
 [ HAVING condition ]
 [ WINDOW window_name AS ( window_definition ) [, ...] ]
 [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] select ]
 [ ORDER BY expression [ ASC | DESC | USING operator ] [ NULLS { FIRST | LAST } ] [, ...] ]
 [ LIMIT { count | ALL } ]
 [ OFFSET start [ ROW | ROWS ] ]
 [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
 [ FOR { UPDATE | SHARE } [ OF table_name [, ...] ] [ NOWAIT ] [...] ]
:::

## Description

`SELECT INTO` creates a new table and fills it with data computed by a query.
The data is not returned to the client, as it is with a normal `SELECT`.
The new table\'s columns have the names and data types associated with the output columns of the `SELECT`.

## Parameters

:::{.dl}
:::{.item term="`TEMPORARY` or `TEMP`"}
If specified, the table is created as a temporary table. Refer to [CREATE TABLE](braised:ref/sql-createtable) for details.
:::{/item}
:::{.item term="`UNLOGGED`"}
If specified, the table is created as an unlogged table. Refer to [CREATE TABLE](braised:ref/sql-createtable) for details.
:::{/item}
:::{.item term="*new_table*"}
The name (optionally schema-qualified) of the table to be created.
:::{/item}
:::{/dl}

All other parameters are described in detail under [SELECT](braised:ref/sql-select).

## Notes

[`CREATE TABLE AS`](#sql-createtableas) is functionally similar to `SELECT INTO`. `CREATE TABLE AS` is the recommended syntax, since this form of `SELECT INTO` is not available in ECPG or PL/pgSQL, because they interpret the `INTO` clause differently.
Furthermore, `CREATE TABLE AS` offers a superset of the functionality provided by `SELECT INTO`.

In contrast to `CREATE TABLE AS`, `SELECT INTO` does not allow specifying properties like a table\'s access method with [USING method](braised:ref/sql-createtable#using-method) or the table\'s tablespace with [TABLESPACE tablespace_name](braised:ref/sql-createtable#tablespace-tablespace-name).
Use `CREATE TABLE AS` if necessary.
Therefore, the default table access method is chosen for the new table.
See [default_table_access_method (string)
      
       default_table_access_method configuration parameter](braised:ref/runtime-config-client#default-table-access-method-string-default-table-access-method-configuration-parameter) for more information.

## Examples

Create a new table `films_recent` consisting of only recent entries from the table `films`:

    SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';

## Compatibility

The SQL standard uses `SELECT INTO` to represent selecting values into scalar variables of a host program, rather than creating a new table.
This indeed is the usage found in ECPG (see [ECPG Embedded SQL in C](#ecpg-embedded-sql-in-c)) and PL/pgSQL (see [PL/pgSQL SQL Procedural Language](#pl-pgsql-sql-procedural-language)).
The PostgreSQL usage of `SELECT INTO` to represent table creation is historical.
Some other SQL implementations also use `SELECT INTO` in this way (but most SQL implementations support `CREATE TABLE AS` instead).
Apart from such compatibility considerations, it is best to use `CREATE TABLE AS` for this purpose in new code.
