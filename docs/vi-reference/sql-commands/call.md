---
title: "CALL"
layout: reference
id: sql-call
description: "invoke a procedure"
---

:::synopsis
CALL name ( [ argument ] [, ...] )
:::

## Description

`CALL` executes a procedure.

If the procedure has any output parameters, then a result row will be returned, containing the values of those parameters.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name (optionally schema-qualified) of the procedure.
:::{/item}
:::{.item term="*argument*"}
An argument expression for the procedure call.

Arguments can include parameter names, using the syntax `name => value`. This works the same as in ordinary function calls; see [Calling Functions](braised:ref/sql-syntax-calling-funcs) for details.

Arguments must be supplied for all procedure parameters that lack defaults, including `OUT` parameters. However, arguments matching `OUT` parameters are not evaluated, so it\'s customary to just write `NULL` for them. (Writing something else for an `OUT` parameter might cause compatibility problems with future PostgreSQL versions.)
:::{/item}
:::{/dl}

## Notes

The user must have `EXECUTE` privilege on the procedure in order to be allowed to invoke it.

To call a function (not a procedure), use `SELECT` instead.

If `CALL` is executed in a transaction block, then the called procedure cannot execute transaction control statements.
Transaction control statements are only allowed if `CALL` is executed in its own transaction.

PL/pgSQL handles output parameters in `CALL` commands differently; see [Calling a Procedure](braised:ref/plpgsql-control-structures#calling-a-procedure).

## Examples

CALL do_db_maintenance();

## Compatibility

`CALL` conforms to the SQL standard, except for the handling of output parameters.
The standard says that users should write variables to receive the values of output parameters.
