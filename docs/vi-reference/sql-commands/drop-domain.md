---
title: "DROP DOMAIN"
layout: reference
id: sql-dropdomain
description: "remove a domain"
---

:::synopsis
DROP DOMAIN [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP DOMAIN` removes a domain.
Only the owner of a domain can remove it.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the domain does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing domain.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the domain (such as table columns), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the domain if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

## Examples

To remove the domain `box`:

    DROP DOMAIN box;

## Compatibility

## Compatibility

This command conforms to the SQL standard, except for the `IF EXISTS` option, which is a PostgreSQL extension.

## See Also

## See Also
