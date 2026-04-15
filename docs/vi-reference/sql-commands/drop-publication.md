---
title: "DROP PUBLICATION"
layout: reference
id: sql-droppublication
description: "remove a publication"
---

:::synopsis
DROP PUBLICATION [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP PUBLICATION` removes an existing publication from the database.

A publication can only be dropped by its owner or a superuser.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the publication does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an existing publication.
:::{/item}
:::{.item term="`CASCADE`; `RESTRICT`"}
These key words do not have any effect, since there are no dependencies on publications.
:::{/item}
:::{/dl}

## Examples

Drop a publication:

    DROP PUBLICATION mypublication;

## Compatibility

`DROP PUBLICATION` is a PostgreSQL extension.
