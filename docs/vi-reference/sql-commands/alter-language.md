---
title: "ALTER LANGUAGE"
layout: reference
id: sql-alterlanguage
description: "change the definition of a procedural language"
---

:::synopsis
ALTER [ PROCEDURAL ] LANGUAGE name RENAME TO new_name
ALTER [ PROCEDURAL ] LANGUAGE name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
:::

## Description

`ALTER LANGUAGE` changes the definition of a procedural language.
The only functionality is to rename the language or assign a new owner.
You must be superuser or owner of the language to use `ALTER LANGUAGE`.

## Parameters

:::{.dl}
:::{.item term="*name*"}
Name of a language
:::{/item}
:::{.item term="*new_name*"}
The new name of the language
:::{/item}
:::{.item term="*new_owner*"}
The new owner of the language
:::{/item}
:::{/dl}

## Compatibility

There is no `ALTER LANGUAGE` statement in the SQL standard.
