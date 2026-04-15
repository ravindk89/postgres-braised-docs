---
title: "ALTER STATISTICS"
layout: reference
id: sql-alterstatistics
description: "change the definition of an extended statistics object"
---

:::synopsis
ALTER STATISTICS name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER STATISTICS name RENAME TO new_name
ALTER STATISTICS name SET SCHEMA new_schema
ALTER STATISTICS name SET STATISTICS { new_target | DEFAULT }
:::

## Description

`ALTER STATISTICS` changes the parameters of an existing extended statistics object.
Any parameters not specifically set in the `ALTER STATISTICS` command retain their prior settings.

You must own the statistics object to use `ALTER STATISTICS`.
To change a statistics object\'s schema, you must also have `CREATE` privilege on the new schema.
To alter the owner, you must be able to `SET ROLE` to the new owning role, and that role must have `CREATE` privilege on the statistics object\'s schema. (These restrictions enforce that altering the owner doesn\'t do anything you couldn\'t do by dropping and recreating the statistics object.
However, a superuser can alter ownership of any statistics object anyway.)

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the statistics object to be altered.
:::{/item}
:::{.item term="*new_owner*"}
The user name of the new owner of the statistics object.
:::{/item}
:::{.item term="*new_name*"}
The new name for the statistics object.
:::{/item}
:::{.item term="*new_schema*"}
The new schema for the statistics object.
:::{/item}
:::{.item term="*new_target*"}
The statistic-gathering target for this statistics object for subsequent [`ANALYZE`](#sql-analyze) operations. The target can be set in the range 0 to 10000. Set it to `DEFAULT` to revert to using the system default statistics target ([default_statistics_target (integer)
      
   default_statistics_target configuration parameter](braised:ref/runtime-config-query#default-statistics-target-integer-default-statistics-target-configuration-parameter)). (Setting to a value of -1 is an obsolete way spelling to get the same outcome.) For more information on the use of statistics by the PostgreSQL query planner, refer to [Statistics Used by the Planner](braised:ref/planner-stats).
:::{/item}
:::{/dl}

## Compatibility

There is no `ALTER STATISTICS` command in the SQL standard.
