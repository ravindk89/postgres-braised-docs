---
title: "DROP MATERIALIZED VIEW"
layout: reference
id: sql-dropmaterializedview
description: "remove a materialized view"
---

:::synopsis
DROP MATERIALIZED VIEW [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP MATERIALIZED VIEW` drops an existing materialized view.
To execute this command you must be the owner of the materialized view.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the materialized view does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the materialized view to remove.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the materialized view (such as other materialized views, or regular views), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the materialized view if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

This command will remove the materialized view called `order_summary`:

    DROP MATERIALIZED VIEW order_summary;

## Compatibility

`DROP MATERIALIZED VIEW` is a PostgreSQL extension.
