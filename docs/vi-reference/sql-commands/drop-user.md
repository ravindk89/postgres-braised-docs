---
title: "DROP USER"
layout: reference
id: sql-dropuser
description: "remove a database role"
---

:::synopsis
DROP USER [ IF EXISTS ] name [, ...]
:::

## Description

`DROP USER` is simply an alternate spelling of [`DROP ROLE`](#sql-droprole).

## Compatibility

The `DROP USER` statement is a PostgreSQL extension.
The SQL standard leaves the definition of users to the implementation.
