---
title: "ALTER SERVER"
layout: reference
id: sql-alterserver
description: "change the definition of a foreign server"
---

:::synopsis
ALTER SERVER name [ VERSION 'new_version' ]
 [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] ) ]
ALTER SERVER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER SERVER name RENAME TO new_name
:::

## Description

`ALTER SERVER` changes the definition of a foreign server.
The first form changes the server version string or the generic options of the server (at least one clause is required).
The second form changes the owner of the server.

To alter the server you must be the owner of the server.
Additionally to alter the owner, you must be able to `SET ROLE` to the new owning role, and you must have `USAGE` privilege on the server\'s foreign-data wrapper. (Note that superusers satisfy all these criteria automatically.)

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of an existing server.
:::{/item}
:::{.item term="*new_version*"}
New server version.
:::{/item}
:::{.item term="`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`"}
Change options for the server. `ADD`, `SET`, and `DROP` specify the action to be performed. `ADD` is assumed if no operation is explicitly specified. Option names must be unique; names and values are also validated using the server\'s foreign-data wrapper library.
:::{/item}
:::{.item term="*new_owner*"}
The user name of the new owner of the foreign server.
:::{/item}
:::{.item term="*new_name*"}
The new name for the foreign server.
:::{/item}
:::{/dl}

## Examples

Alter server `foo`, add connection options:

    ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');

Alter server `foo`, change version, change `host` option:

    ALTER SERVER foo VERSION '8.4' OPTIONS (SET host 'baz');

## Compatibility

`ALTER SERVER` conforms to ISO/IEC 9075-9 (SQL/MED).
The `OWNER TO` and `RENAME` forms are PostgreSQL extensions.
