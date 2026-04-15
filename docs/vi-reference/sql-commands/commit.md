---
title: "COMMIT"
layout: reference
id: sql-commit
description: "commit the current transaction"
---

:::synopsis
COMMIT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
:::

## Description

`COMMIT` commits the current transaction.
All changes made by the transaction become visible to others and are guaranteed to be durable if a crash occurs.

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

Use [ROLLBACK](braised:ref/sql-rollback) to abort a transaction.

Issuing `COMMIT` when not inside a transaction does no harm, but it will provoke a warning message. `COMMIT AND CHAIN` when not inside a transaction is an error.

## Examples

To commit the current transaction and make all changes permanent:

    COMMIT;

## Compatibility

The command `COMMIT` conforms to the SQL standard.
The form `COMMIT TRANSACTION` is a PostgreSQL extension.
