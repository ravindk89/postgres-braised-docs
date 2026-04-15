---
title: "DEALLOCATE"
layout: reference
id: sql-deallocate
description: "deallocate a prepared statement"
---

:::synopsis
DEALLOCATE [ PREPARE ] { name | ALL }
:::

## Description

`DEALLOCATE` is used to deallocate a previously prepared SQL statement.
If you do not explicitly deallocate a prepared statement, it is deallocated when the session ends.

For more information on prepared statements, see [PREPARE](braised:ref/sql-prepare).

## Parameters

:::{.dl}
:::{.item term="`PREPARE`"}
This key word is ignored.
:::{/item}
:::{.item term="*name*"}
The name of the prepared statement to deallocate.
:::{/item}
:::{.item term="`ALL`"}
Deallocate all prepared statements.
:::{/item}
:::{/dl}

## Compatibility

The SQL standard includes a `DEALLOCATE` statement, but it is only for use in embedded SQL.
