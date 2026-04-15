---
title: "RESET"
layout: reference
id: sql-reset
description: "restore the value of a run-time parameter to the default value"
---

:::synopsis
RESET configuration_parameter
RESET ALL
:::

## Description

`RESET` restores run-time parameters to their default values. `RESET` is an alternative spelling for SET *configuration_parameter* TO DEFAULT Refer to [SET](braised:ref/sql-set) for details.

The default value is defined as the value that the parameter would have had, if no `SET` had ever been issued for it in the current session.
The actual source of this value might be a compiled-in default, the configuration file, command-line options, or per-database or per-user default settings.
This is subtly different from defining it as "the value that the parameter had at session start", because if the value came from the configuration file, it will be reset to whatever is specified by the configuration file now.
See [Server Configuration](#server-configuration) for details.

The transactional behavior of `RESET` is the same as `SET`: its effects will be undone by transaction rollback.

## Parameters

:::{.dl}
:::{.item term="*configuration_parameter*"}
Name of a settable run-time parameter. Available parameters are documented in [Server Configuration](#server-configuration) and on the [SET](braised:ref/sql-set) reference page.
:::{/item}
:::{.item term="`ALL`"}
Resets all settable run-time parameters to default values.
:::{/item}
:::{/dl}

## Examples

Set the `timezone` configuration variable to its default value:

    RESET timezone;

## Compatibility

`RESET` is a PostgreSQL extension.
