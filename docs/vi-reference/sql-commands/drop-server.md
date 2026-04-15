---
title: "DROP SERVER"
layout: reference
id: sql-dropserver
description: "remove a foreign server descriptor"
---

:::synopsis
DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP SERVER` removes an existing foreign server descriptor.
To execute this command, the current user must be the owner of the server.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the server does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an existing server.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the server (such as user mappings), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the server if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Drop a server `foo` if it exists:

    DROP SERVER IF EXISTS foo;

## Compatibility

`DROP SERVER` conforms to ISO/IEC 9075-9 (SQL/MED).
The `IF EXISTS` clause is a PostgreSQL extension.
