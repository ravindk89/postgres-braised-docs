---
title: "ALTER FOREIGN DATA WRAPPER"
layout: reference
id: sql-alterforeigndatawrapper
description: "change the definition of a foreign-data wrapper"
---

:::synopsis
ALTER FOREIGN DATA WRAPPER name
 [ HANDLER handler_function | NO HANDLER ]
 [ VALIDATOR validator_function | NO VALIDATOR ]
 [ OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ]) ]
ALTER FOREIGN DATA WRAPPER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER FOREIGN DATA WRAPPER name RENAME TO new_name
:::

## Description

`ALTER FOREIGN DATA WRAPPER` changes the definition of a foreign-data wrapper.
The first form of the command changes the support functions or the generic options of the foreign-data wrapper (at least one clause is required).
The second form changes the owner of the foreign-data wrapper.

Only superusers can alter foreign-data wrappers.
Additionally, only superusers can own foreign-data wrappers.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of an existing foreign-data wrapper.
:::{/item}
:::{.item term="`HANDLER handler_function`"}
Specifies a new handler function for the foreign-data wrapper.
:::{/item}
:::{.item term="`NO HANDLER`"}
This is used to specify that the foreign-data wrapper should no longer have a handler function.

Note that foreign tables that use a foreign-data wrapper with no handler cannot be accessed.
:::{/item}
:::{.item term="`VALIDATOR validator_function`"}
Specifies a new validator function for the foreign-data wrapper.

Note that it is possible that pre-existing options of the foreign-data wrapper, or of dependent servers, user mappings, or foreign tables, are invalid according to the new validator. PostgreSQL does not check for this. It is up to the user to make sure that these options are correct before using the modified foreign-data wrapper. However, any options specified in this `ALTER FOREIGN DATA WRAPPER` command will be checked using the new validator.
:::{/item}
:::{.item term="`NO VALIDATOR`"}
This is used to specify that the foreign-data wrapper should no longer have a validator function.
:::{/item}
:::{.item term="`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`"}
Change options for the foreign-data wrapper. `ADD`, `SET`, and `DROP` specify the action to be performed. `ADD` is assumed if no operation is explicitly specified. Option names must be unique; names and values are also validated using the foreign data wrapper\'s validator function, if any.
:::{/item}
:::{.item term="*new_owner*"}
The user name of the new owner of the foreign-data wrapper.
:::{/item}
:::{.item term="*new_name*"}
The new name for the foreign-data wrapper.
:::{/item}
:::{/dl}

## Examples

Change a foreign-data wrapper `dbi`, add option `foo`, drop `bar`:

    ALTER FOREIGN DATA WRAPPER dbi OPTIONS (ADD foo '1', DROP bar);

Change the foreign-data wrapper `dbi` validator to `bob.myvalidator`:

    ALTER FOREIGN DATA WRAPPER dbi VALIDATOR bob.myvalidator;

## Compatibility

`ALTER FOREIGN DATA WRAPPER` conforms to ISO/IEC 9075-9 (SQL/MED), except that the `HANDLER`, `VALIDATOR`, `OWNER TO`, and `RENAME` clauses are extensions.
