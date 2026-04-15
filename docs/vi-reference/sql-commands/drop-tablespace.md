---
title: "DROP TABLESPACE"
layout: reference
id: sql-droptablespace
description: "remove a tablespace"
---

:::synopsis
DROP TABLESPACE [ IF EXISTS ] name
:::

## Description

`DROP TABLESPACE` removes a tablespace from the system.

A tablespace can only be dropped by its owner or a superuser.
The tablespace must be empty of all database objects before it can be dropped.
It is possible that objects in other databases might still reside in the tablespace even if no objects in the current database are using the tablespace.
Also, if the tablespace is listed in the [temp_tablespaces (string)
      
       temp_tablespaces configuration parameter
      
      tablespacetemporary](braised:ref/runtime-config-client#temp-tablespaces-string-temp-tablespaces-configuration-parameter-tablespacetemporary) setting of any active session, the `DROP` might fail due to temporary files residing in the tablespace.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the tablespace does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of a tablespace.
:::{/item}
:::{/dl}

## Notes

`DROP TABLESPACE` cannot be executed inside a transaction block.

## Examples

To remove tablespace `mystuff` from the system:

    DROP TABLESPACE mystuff;

## Compatibility

`DROP TABLESPACE` is a PostgreSQL extension.
