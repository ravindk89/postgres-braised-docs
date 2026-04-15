---
title: "SHOW"
layout: reference
id: sql-show
description: "show the value of a run-time parameter"
---

:::synopsis
SHOW name
SHOW ALL
:::

## Description

`SHOW` will display the current setting of run-time parameters.
These variables can be set using the `SET` statement, by editing the `postgresql.conf` configuration file, through the `PGOPTIONS` environmental variable (when using libpq or a libpq-based application), or through command-line flags when starting the `postgres` server.
See [Server Configuration](#server-configuration) for details.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of a run-time parameter. Available parameters are documented in [Server Configuration](#server-configuration) and on the [SET](braised:ref/sql-set) reference page. In addition, there are a few parameters that can be shown but not set:

`SERVER_VERSION`

:   Shows the server\'s version number.

`SERVER_ENCODING`

:   Shows the server-side character set encoding. At present, this parameter can be shown but not set, because the encoding is determined at database creation time.

`IS_SUPERUSER`

:   True if the current role has superuser privileges.
:::{/item}
:::{.item term="`ALL`"}
Show the values of all configuration parameters, with descriptions.
:::{/item}
:::{/dl}

## Notes

The function `current_setting` produces equivalent output; see [Configuration Settings Functions](braised:ref/functions-admin#configuration-settings-functions).
Also, the [pg_settings](#view-pg-settings) system view produces the same information.

## Examples

Show the current setting of the parameter `DateStyle`:

    SHOW DateStyle;
     DateStyle
    -----------
     ISO, MDY
    (1 row)

Show the current setting of the parameter `geqo`:

    SHOW geqo;
     geqo
    ------
     on
    (1 row)

Show all settings:

    SHOW ALL;
                name         | setting |                description
    -------------------------+---------+-------------------------------------------------
     allow_system_table_mods | off     | Allows modifications of the structure of ...
        .
        .
        .
     xmloption               | content | Sets whether XML data in implicit parsing ...
     zero_damaged_pages      | off     | Continues processing past damaged page headers.
    (196 rows)

## Compatibility

The `SHOW` command is a PostgreSQL extension.
