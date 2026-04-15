---
title: "CHECKPOINT"
layout: reference
id: sql-checkpoint
description: "force a write-ahead log checkpoint"
---

:::synopsis
CHECKPOINT
:::

## Description

A checkpoint is a point in the write-ahead log sequence at which all data files have been updated to reflect the information in the log.
All data files will be flushed to disk.
Refer to [WAL Configuration](braised:ref/wal-configuration) for more details about what happens during a checkpoint.

The `CHECKPOINT` command forces an immediate checkpoint when the command is issued, without waiting for a regular checkpoint scheduled by the system (controlled by the settings in [Checkpoints](braised:ref/runtime-config-wal#checkpoints)). `CHECKPOINT` is not intended for use during normal operation.

If executed during recovery, the `CHECKPOINT` command will force a restartpoint (see [WAL Configuration](braised:ref/wal-configuration)) rather than writing a new checkpoint.

Only superusers or users with the privileges of the [pg_checkpoint](braised:ref/predefined-roles#pg-checkpoint) role can call `CHECKPOINT`.

## Compatibility

The `CHECKPOINT` command is a PostgreSQL language extension.
