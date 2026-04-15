---
title: "DROP COLLATION"
layout: reference
id: sql-dropcollation
description: "remove a collation"
---

:::synopsis
DROP COLLATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

## Description

`DROP COLLATION` removes a previously defined collation.
To be able to drop a collation, you must own the collation.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the collation does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of the collation. The collation name can be schema-qualified.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the collation, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the collation if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

## Examples

To drop the collation named `german`:

    DROP COLLATION german;

## Compatibility

## Compatibility

The `DROP COLLATION` command conforms to the SQL standard, apart from the `IF EXISTS` option, which is a PostgreSQL extension.
