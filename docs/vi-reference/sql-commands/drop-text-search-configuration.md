---
title: "DROP TEXT SEARCH CONFIGURATION"
layout: reference
id: sql-droptsconfig
description: "remove a text search configuration"
---

:::synopsis
DROP TEXT SEARCH CONFIGURATION [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

`DROP TEXT SEARCH CONFIGURATION` drops an existing text search configuration.
To execute this command you must be the owner of the configuration.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the text search configuration does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing text search configuration.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the text search configuration, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the text search configuration if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Remove the text search configuration `my_english`:

    DROP TEXT SEARCH CONFIGURATION my_english;

This command will not succeed if there are any existing indexes that reference the configuration in `to_tsvector` calls.
Add `CASCADE` to drop such indexes along with the text search configuration.

## Compatibility

There is no `DROP TEXT SEARCH CONFIGURATION` statement in the SQL standard.
