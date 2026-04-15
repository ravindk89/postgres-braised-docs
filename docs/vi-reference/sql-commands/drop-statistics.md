---
title: "DROP STATISTICS"
layout: reference
id: sql-dropstatistics
description: "remove extended statistics"
---

:::synopsis
DROP STATISTICS [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP STATISTICS` removes statistics object(s) from the database.
Only the statistics object\'s owner, the schema owner, or a superuser can drop a statistics object.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the statistics object does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the statistics object to drop.
:::{/item}
:::{.item term="`CASCADE`; `RESTRICT`"}
These key words do not have any effect, since there are no dependencies on statistics.
:::{/item}
:::{/dl}

## Examples

To destroy two statistics objects in different schemas, without failing if they don\'t exist:

    DROP STATISTICS IF EXISTS
        accounting.users_uid_creation,
        public.grants_user_role;

## Compatibility

There is no `DROP STATISTICS` command in the SQL standard.
