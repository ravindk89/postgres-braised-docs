---
title: "DROP TYPE"
layout: reference
id: sql-droptype
description: "remove a data type"
---

:::synopsis
DROP TYPE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP TYPE` removes a user-defined data type.
Only the owner of a type can remove it.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the type does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the data type to remove.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the type (such as table columns, functions, and operators), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the type if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

## Examples

To remove the data type `box`:

    DROP TYPE box;

## Compatibility

## Compatibility

This command is similar to the corresponding command in the SQL standard, apart from the `IF EXISTS` option, which is a PostgreSQL extension.
But note that much of the `CREATE TYPE` command and the data type extension mechanisms in PostgreSQL differ from the SQL standard.

## See Also

## See Also
