---
title: "DROP TEXT SEARCH TEMPLATE"
layout: reference
id: sql-droptstemplate
description: "remove a text search template"
---

:::synopsis
DROP TEXT SEARCH TEMPLATE [ IF EXISTS ] name [ CASCADE | RESTRICT ]
:::

## Description

`DROP TEXT SEARCH TEMPLATE` drops an existing text search template.
You must be a superuser to use this command.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the text search template does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing text search template.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the text search template, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the text search template if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Remove the text search template `thesaurus`:

    DROP TEXT SEARCH TEMPLATE thesaurus;

This command will not succeed if there are any existing text search dictionaries that use the template.
Add `CASCADE` to drop such dictionaries along with the template.

## Compatibility

There is no `DROP TEXT SEARCH TEMPLATE` statement in the SQL standard.
