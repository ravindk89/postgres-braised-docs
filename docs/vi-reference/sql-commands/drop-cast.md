---
title: "DROP CAST"
layout: reference
id: sql-dropcast
description: "remove a cast"
---

:::synopsis
DROP CAST [ IF EXISTS ] (source_type AS target_type) [ CASCADE | RESTRICT ]
:::

## Description

## Description

`DROP CAST` removes a previously defined cast.

To be able to drop a cast, you must own the source or the target data type.
These are the same privileges that are required to create a cast.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the cast does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*source_type*"}
The name of the source data type of the cast.
:::{/item}
:::{.item term="*target_type*"}
The name of the target data type of the cast.
:::{/item}
:::{.item term="`CASCADE`; `RESTRICT`"}
These key words do not have any effect, since there are no dependencies on casts.
:::{/item}
:::{/dl}

## Examples

## Examples

To drop the cast from type `text` to type `int`:

    DROP CAST (text AS int);

## Compatibility

## Compatibility

The `DROP CAST` command conforms to the SQL standard.
