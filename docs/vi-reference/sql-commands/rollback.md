---
title: "ROLLBACK"
layout: reference
id: sql-rollback
description: "abort the current transaction"
---

:::synopsis
ROLLBACK [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
:::

## Description

`ROLLBACK` rolls back the current transaction and causes all the updates made by the transaction to be discarded.

## Parameters

:::{.dl}
:::{.item term="`WORK`; `TRANSACTION`"}
Optional key words. They have no effect.
:::{/item}
:::{.item term="`AND CHAIN`"}
If `AND CHAIN` is specified, a new (not aborted) transaction is immediately started with the same transaction characteristics (see [SET TRANSACTION](braised:ref/sql-set-transaction)) as the just finished one. Otherwise, no new transaction is started.
:::{/item}
:::{/dl}

## Notes

Use [`COMMIT`](#sql-commit) to successfully terminate a transaction.

Issuing `ROLLBACK` outside of a transaction block emits a warning and otherwise has no effect. `ROLLBACK AND CHAIN` outside of a transaction block is an error.

## Examples

To abort all changes:

    ROLLBACK;

## Compatibility

The command `ROLLBACK` conforms to the SQL standard.
The form `ROLLBACK TRANSACTION` is a PostgreSQL extension.
