---
title: "DROP LANGUAGE"
layout: reference
id: sql-droplanguage
description: "remove a procedural language"
---

:::synopsis
DROP [ PROCEDURAL ] LANGUAGE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

`DROP LANGUAGE` removes the definition of a previously registered procedural language.
You must be a superuser or the owner of the language to use `DROP LANGUAGE`.

:::{.callout type="note"}
As of PostgreSQL 9.1, most procedural languages have been made into "extensions", and should therefore be removed with [`DROP EXTENSION`](#sql-dropextension) not `DROP LANGUAGE`.
:::

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the language does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name of an existing procedural language.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the language (such as functions in the language), and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the language if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

This command removes the procedural language `plsample`:

    DROP LANGUAGE plsample;

## Compatibility

There is no `DROP LANGUAGE` statement in the SQL standard.
