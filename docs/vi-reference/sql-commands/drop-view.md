---
title: "DROP VIEW"
layout: reference
id: sql-dropview
description: "remove a view"
---

:::synopsis
DROP VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP VIEW` drops an existing view.
To execute this command you must be the owner of the view.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the view does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the view to remove.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the view (such as other views), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the view if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

This command will remove the view called `kinds`:

    DROP VIEW kinds;

## Compatibility

This command conforms to the SQL standard, except that the standard only allows one view to be dropped per command, and apart from the `IF EXISTS` option, which is a PostgreSQL extension.
