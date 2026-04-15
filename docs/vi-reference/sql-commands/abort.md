---
title: "ABORT"
layout: reference
id: sql-abort
description: "abort the current transaction"
---

:::synopsis
ABORT [ WORK | TRANSACTION ] [ AND [ NO ] CHAIN ]
:::

## Description

`ABORT` rolls back the current transaction and causes all the updates made by the transaction to be discarded.
This command is identical in behavior to the standard SQL command [`ROLLBACK`](#sql-rollback), and is present only for historical reasons.

## Parameters

:::{.dl}
:::{.item term="`WORK`; `TRANSACTION`"}
Optional key words. They have no effect.
:::{/item}
:::{.item term="`AND CHAIN`"}
If `AND CHAIN` is specified, a new transaction is immediately started with the same transaction characteristics (see [`SET TRANSACTION`](#sql-set-transaction)) as the just finished one. Otherwise, no new transaction is started.
:::{/item}
:::{/dl}

## Notes

Use [`COMMIT`](#sql-commit) to successfully terminate a transaction.

Issuing `ABORT` outside of a transaction block emits a warning and otherwise has no effect.

## Examples

To abort all changes:

    ABORT;

## Compatibility

This command is a PostgreSQL extension present for historical reasons. `ROLLBACK` is the equivalent standard SQL command.
