---
title: "ALTER TEXT SEARCH TEMPLATE"
layout: reference
id: sql-altertstemplate
description: "change the definition of a text search template"
---

:::synopsis
ALTER TEXT SEARCH TEMPLATE name RENAME TO new_name
ALTER TEXT SEARCH TEMPLATE name SET SCHEMA new_schema
:::

## Description

`ALTER TEXT SEARCH TEMPLATE` changes the definition of a text search template.
Currently, the only supported functionality is to change the template\'s name.

You must be a superuser to use `ALTER TEXT SEARCH TEMPLATE`.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing text search template.
:::{/item}
:::{.item term="*new_name*"}
The new name of the text search template.
:::{/item}
:::{.item term="*new_schema*"}
The new schema for the text search template.
:::{/item}
:::{/dl}

## Compatibility

There is no `ALTER TEXT SEARCH TEMPLATE` statement in the SQL standard.
