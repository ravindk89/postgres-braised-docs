---
title: "DROP TRIGGER"
layout: reference
id: sql-droptrigger
description: "remove a trigger"
---

:::synopsis
DROP TRIGGER [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
:::

## Description

`DROP TRIGGER` removes an existing trigger definition.
To execute this command, the current user must be the owner of the table for which the trigger is defined.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the trigger does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of the trigger to remove.
:::{/item}
:::{.item term="*table_name*"}
The name (optionally schema-qualified) of the table for which the trigger is defined.
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

Destroy the trigger `if_dist_exists` on the table `films`:

    DROP TRIGGER if_dist_exists ON films;

## Compatibility

## Compatibility

The `DROP TRIGGER` statement in PostgreSQL is incompatible with the SQL standard.
In the SQL standard, trigger names are not local to tables, so the command is simply `DROP TRIGGER name`.
