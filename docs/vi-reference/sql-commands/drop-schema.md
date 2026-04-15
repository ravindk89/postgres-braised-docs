---
title: "DROP SCHEMA"
layout: reference
id: sql-dropschema
description: "remove a schema"
---

:::synopsis
DROP SCHEMA [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP SCHEMA` removes schemas from the database.

A schema can only be dropped by its owner or a superuser.
Note that the owner can drop the schema (and thereby all contained objects) even if they do not own some of the objects within the schema.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the schema does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of a schema.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects (tables, functions, etc.) that are contained in the schema, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the schema if it contains any objects. This is the default.
:::{/item}
:::{/dl}

## Notes

Using the `CASCADE` option might make the command remove objects in other schemas besides the one(s) named.

## Examples

To remove schema `mystuff` from the database, along with everything it contains:

    DROP SCHEMA mystuff CASCADE;

## Compatibility

`DROP SCHEMA` is fully conforming with the SQL standard, except that the standard only allows one schema to be dropped per command, and apart from the `IF EXISTS` option, which is a PostgreSQL extension.
