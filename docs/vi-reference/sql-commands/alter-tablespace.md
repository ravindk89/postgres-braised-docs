---
title: "ALTER TABLESPACE"
layout: reference
id: sql-altertablespace
description: "change the definition of a tablespace"
---

:::synopsis
ALTER TABLESPACE name RENAME TO new_name
ALTER TABLESPACE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER TABLESPACE name SET ( tablespace_option = value [, ... ] )
ALTER TABLESPACE name RESET ( tablespace_option [, ... ] )
:::

## Description

`ALTER TABLESPACE` can be used to change the definition of a tablespace.

You must own the tablespace to change the definition of a tablespace.
To alter the owner, you must also be able to `SET ROLE` to the new owning role. (Note that superusers have these privileges automatically.)

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of an existing tablespace.
:::{/item}
:::{.item term="*new_name*"}
The new name of the tablespace. The new name cannot begin with `pg_`, as such names are reserved for system tablespaces.
:::{/item}
:::{.item term="*new_owner*"}
The new owner of the tablespace.
:::{/item}
:::{.item term="*tablespace_option*"}
A tablespace parameter to be set or reset. Currently, the only available parameters are `seq_page_cost`, `random_page_cost`, `effective_io_concurrency` and `maintenance_io_concurrency`. Setting these values for a particular tablespace will override the planner\'s usual estimate of the cost of reading pages from tables in that tablespace, and how many concurrent I/Os are issued, as established by the configuration parameters of the same name (see [seq_page_cost (floating point)
      
   seq_page_cost configuration parameter](braised:ref/runtime-config-query#seq-page-cost-floating-point-seq-page-cost-configuration-parameter), [random_page_cost (floating point)
      
   random_page_cost configuration parameter](braised:ref/runtime-config-query#random-page-cost-floating-point-random-page-cost-configuration-parameter), [effective_io_concurrency (integer)
       
    effective_io_concurrency configuration parameter](braised:ref/runtime-config-resource#effective-io-concurrency-integer-effective-io-concurrency-configuration-parameter), [maintenance_io_concurrency (integer)
       
    maintenance_io_concurrency configuration parameter](braised:ref/runtime-config-resource#maintenance-io-concurrency-integer-maintenance-io-concurrency-configuration-parameter)). This may be useful if one tablespace is located on a disk which is faster or slower than the remainder of the I/O subsystem.
:::{/item}
:::{/dl}

## Examples

Rename tablespace `index_space` to `fast_raid`:

    ALTER TABLESPACE index_space RENAME TO fast_raid;

Change the owner of tablespace `index_space`:

    ALTER TABLESPACE index_space OWNER TO mary;

## Compatibility

There is no `ALTER TABLESPACE` statement in the SQL standard.
