---
title: "DROP RULE"
layout: reference
id: sql-droprule
description: "remove a rewrite rule"
---

:::synopsis
DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
:::

## Description

`DROP RULE` drops a rewrite rule.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the rule does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of the rule to drop.
:::{/item}
:::{.item term="*table_name*"}
The name (optionally schema-qualified) of the table or view that the rule applies to.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the rule, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the rule if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

To drop the rewrite rule `newrule`:

    DROP RULE newrule ON mytable;

## Compatibility

`DROP RULE` is a PostgreSQL language extension, as is the entire query rewrite system.
