---
title: "ALTER RULE"
layout: reference
id: sql-alterrule
description: "change the definition of a rule"
---

:::synopsis
ALTER RULE name ON table_name RENAME TO new_name
:::

## Description

`ALTER RULE` changes properties of an existing rule.
Currently, the only available action is to change the rule\'s name.

To use `ALTER RULE`, you must own the table or view that the rule applies to.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of an existing rule to alter.
:::{/item}
:::{.item term="*table_name*"}
The name (optionally schema-qualified) of the table or view that the rule applies to.
:::{/item}
:::{.item term="*new_name*"}
The new name for the rule.
:::{/item}
:::{/dl}

## Examples

To rename an existing rule:

    ALTER RULE notify_all ON emp RENAME TO notify_me;

## Compatibility

`ALTER RULE` is a PostgreSQL language extension, as is the entire query rewrite system.
