---
title: "ALTER OPERATOR CLASS"
layout: reference
id: sql-alteropclass
description: "change the definition of an operator class"
---

:::synopsis
ALTER OPERATOR CLASS name USING index_method
 RENAME TO new_name

ALTER OPERATOR CLASS name USING index_method
 OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }

ALTER OPERATOR CLASS name USING index_method
 SET SCHEMA new_schema
:::

## Description

`ALTER OPERATOR CLASS` changes the definition of an operator class.

You must own the operator class to use `ALTER OPERATOR CLASS`.
To alter the owner, you must be able to `SET ROLE` to the new owning role, and that role must have `CREATE` privilege on the operator class\'s schema. (These restrictions enforce that altering the owner doesn\'t do anything you couldn\'t do by dropping and recreating the operator class.
However, a superuser can alter ownership of any operator class anyway.)

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing operator class.
:::{/item}
:::{.item term="*index_method*"}
The name of the index method this operator class is for.
:::{/item}
:::{.item term="*new_name*"}
The new name of the operator class.
:::{/item}
:::{.item term="*new_owner*"}
The new owner of the operator class.
:::{/item}
:::{.item term="*new_schema*"}
The new schema for the operator class.
:::{/item}
:::{/dl}

## Compatibility

There is no `ALTER OPERATOR CLASS` statement in the SQL standard.
