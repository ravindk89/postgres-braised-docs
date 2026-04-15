---
title: "DROP EVENT TRIGGER"
layout: reference
id: sql-dropeventtrigger
description: "remove an event trigger"
---

:::synopsis
DROP EVENT TRIGGER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

`DROP EVENT TRIGGER` removes an existing event trigger.
To execute this command, the current user must be the owner of the event trigger.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the event trigger does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of the event trigger to remove.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the trigger, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the trigger if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

## Examples

Destroy the trigger `snitch`:

    DROP EVENT TRIGGER snitch;

## Compatibility

## Compatibility

There is no `DROP EVENT TRIGGER` statement in the SQL standard.
