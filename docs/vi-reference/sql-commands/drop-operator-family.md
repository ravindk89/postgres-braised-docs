---
title: "DROP OPERATOR FAMILY"
layout: reference
id: sql-dropopfamily
description: "remove an operator family"
---

:::synopsis
DROP OPERATOR FAMILY [ IF EXISTS ] name USING index_method [ CASCADE | RESTRICT ]
:::

## Description

`DROP OPERATOR FAMILY` drops an existing operator family.
To execute this command you must be the owner of the operator family.

`DROP OPERATOR FAMILY` includes dropping any operator classes contained in the family, but it does not drop any of the operators or functions referenced by the family.
If there are any indexes depending on operator classes within the family, you will need to specify `CASCADE` for the drop to complete.

## Parameters

:::{.dl}
:::{.item term="`IF EXISTS`"}
Do not throw an error if the operator family does not exist. A notice is issued in this case.
:::{/item}
:::{.item term="*name*"}
The name (optionally schema-qualified) of an existing operator family.
:::{/item}
:::{.item term="*index_method*"}
The name of the index access method the operator family is for.
:::{/item}
:::{.item term="`CASCADE`"}
Automatically drop objects that depend on the operator family, and in turn all objects that depend on those objects (see [Dependency Tracking](braised:ref/ddl-depend)).
:::{/item}
:::{.item term="`RESTRICT`"}
Refuse to drop the operator family if any objects depend on it. This is the default.
:::{/item}
:::{/dl}

## Examples

Remove the B-tree operator family `float_ops`:

    DROP OPERATOR FAMILY float_ops USING btree;

This command will not succeed if there are any existing indexes that use operator classes within the family.
Add `CASCADE` to drop such indexes along with the operator family.

## Compatibility

There is no `DROP OPERATOR FAMILY` statement in the SQL standard.
