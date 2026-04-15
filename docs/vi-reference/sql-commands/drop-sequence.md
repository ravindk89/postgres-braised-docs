---
title: "DROP SEQUENCE"
layout: reference
id: sql-dropsequence
description: "remove a sequence"
---

:::synopsis
DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
:::

## Description

`DROP SEQUENCE` removes sequence number generators.
A sequence can only be dropped by its owner or a superuser.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the sequence does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of a sequence.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the sequence, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the sequence if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

To remove the sequence `serial`:

    DROP SEQUENCE serial;

## Compatibility

`DROP SEQUENCE` conforms to the SQL standard, except that the standard only allows one sequence to be dropped per command, and apart from the `IF EXISTS` option, which is a PostgreSQL extension.
