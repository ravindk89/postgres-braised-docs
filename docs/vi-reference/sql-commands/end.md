---
title: "END"
layout: reference
id: sql-end
description: "commit the current transaction"
---

:::synopsis
END [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
:::

## Description

`END` commits the current transaction.
All changes made by the transaction become visible to others and are guaranteed to be durable if a crash occurs.
This command is a PostgreSQL extension that is equivalent to [`COMMIT`](#sql-commit).

## Parameters

:::{.dl}
:::{.item term="`WORK`; `TRANSACTION`"}
Optional key words. They have no effect.
:::{/item}
:::{.item term="`AND CHAIN`"}
If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](braised:ref/sql-set-transaction)) as the just finished one. Otherwise, no new transaction is started.
:::{/item}
:::{/dl}

## Notes

Use [`ROLLBACK`](#sql-rollback) to abort a transaction.

Issuing `END` when not inside a transaction does no harm, but it will provoke a warning message.

## Examples

To commit the current transaction and make all changes permanent:

    END;

## Compatibility

`END` is a PostgreSQL extension that provides functionality equivalent to [`COMMIT`](#sql-commit), which is specified in the SQL standard.
