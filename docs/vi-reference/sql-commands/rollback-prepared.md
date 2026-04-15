---
title: "ROLLBACK PREPARED"
layout: reference
id: sql-rollback-prepared
description: "cancel a transaction that was earlier prepared for two-phase commit"
---

:::synopsis
ROLLBACK PREPARED transaction_id
:::

## Description

`ROLLBACK PREPARED` rolls back a transaction that is in prepared state.

## Parameters

:::{.dl}
:::{.item term="*transaction_id*"}
The transaction identifier of the transaction that is to be rolled back.
:::{/item}
:::{/dl}

## Notes

To roll back a prepared transaction, you must be either the same user that executed the transaction originally, or a superuser.
But you do not have to be in the same session that executed the transaction.

This command cannot be executed inside a transaction block.
The prepared transaction is rolled back immediately.

All currently available prepared transactions are listed in the [pg_prepared_xacts](#view-pg-prepared-xacts) system view.

## Examples

## Examples

Roll back the transaction identified by the transaction identifier `foobar`:

    ROLLBACK PREPARED 'foobar';

## Compatibility

`ROLLBACK PREPARED` is a PostgreSQL extension.
It is intended for use by external transaction management systems, some of which are covered by standards (such as X/Open XA), but the SQL side of those systems is not standardized.
