---
title: "DROP FOREIGN DATA WRAPPER"
layout: reference
id: sql-dropforeigndatawrapper
description: "remove a foreign-data wrapper"
---

:::synopsis
DROP FOREIGN DATA WRAPPER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP FOREIGN DATA WRAPPER` removes an existing foreign-data wrapper.
To execute this command, the current user must be the owner of the foreign-data wrapper.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the foreign-data wrapper does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an existing foreign-data wrapper.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the foreign-data wrapper (such as foreign tables and servers), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the foreign-data wrapper if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Drop the foreign-data wrapper `dbi`:

    DROP FOREIGN DATA WRAPPER dbi;

## Compatibility

`DROP FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED).
The `IF EXISTS` clause is a PostgreSQL extension.
