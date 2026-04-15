---
title: "DROP TRANSFORM"
layout: reference
id: sql-droptransform
description: "remove a transform"
---

:::synopsis
DROP TRANSFORM [ IF EXISTS ] FOR type_name LANGUAGE lang_name [ CASCADE | RESTRICT ]
:::

## Description

## Description

`DROP TRANSFORM` removes a previously defined transform.

To be able to drop a transform, you must own the type and the language.
These are the same privileges that are required to create a transform.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the transform does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*type_name*"}
The name of the data type of the transform.
:::{/item}
:::{.item term="*lang_name*"}
The name of the language of the transform.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the transform, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the transform if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

## Examples

To drop the transform for type `hstore` and language `plpython3u`:

    DROP TRANSFORM FOR hstore LANGUAGE plpython3u;

## Compatibility

## Compatibility

This form of `DROP TRANSFORM` is a PostgreSQL extension.
See [CREATE TRANSFORM](braised:ref/sql-createtransform) for details.
