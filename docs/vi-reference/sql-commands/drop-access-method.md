---
title: "DROP ACCESS METHOD"
layout: reference
id: sql-drop-access-method
description: "remove an access method"
---

:::synopsis
DROP ACCESS METHOD [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

`DROP ACCESS METHOD` removes an existing access method.
Only superusers can drop access methods.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the access method does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an existing access method.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the access method (such as operator classes, operator families, and indexes), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the access method if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Drop the access method `heptree`:

    DROP ACCESS METHOD heptree;

## Compatibility

`DROP ACCESS METHOD` is a PostgreSQL extension.
