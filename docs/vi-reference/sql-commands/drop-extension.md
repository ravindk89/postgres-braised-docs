---
title: "DROP EXTENSION"
layout: reference
id: sql-dropextension
description: "remove an extension"
---

:::synopsis
DROP EXTENSION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP EXTENSION` removes extensions from the database.
Dropping an extension causes its member objects, and other explicitly dependent routines (see [ALTER ROUTINE](braised:ref/sql-alterroutine), the `DEPENDS ON EXTENSION extension_name` action), to be dropped as well.

You must own the extension to use `DROP EXTENSION`.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the extension does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an installed extension.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the extension, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
This option prevents the specified extensions from being dropped if other objects, besides these extensions, their members, and their explicitly dependent routines, depend on them. This is the default.
:::{/item}
:::{/dl}

## Examples

To remove the extension `hstore` from the current database:

    DROP EXTENSION hstore;

This command will fail if any of `hstore`\'s objects are in use in the database, for example if any tables have columns of the `hstore` type.
Add the `CASCADE` option to forcibly remove those dependent objects as well.

## Compatibility

`DROP EXTENSION` is a PostgreSQL extension.
