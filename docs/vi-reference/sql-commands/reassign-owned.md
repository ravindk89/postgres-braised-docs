---
title: "REASSIGN OWNED"
layout: reference
id: sql-reassign-owned
description: "change the ownership of database objects owned by a database role"
---

:::synopsis
REASSIGN OWNED BY { old_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...]
 TO { new_role | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
:::

## Description

`REASSIGN OWNED` instructs the system to change the ownership of database objects owned by any of the *old_roles* to *new_role*.

## Parameters

:::{.dl}
:::{.item term="*old_role*"}
The name of a role. The ownership of all the objects within the current database, and of all shared objects (databases, tablespaces), owned by this role will be reassigned to *new_role*.
:::{/item}
:::{.item term="*new_role*"}
The name of the role that will be made the new owner of the affected objects.
:::{/item}
:::{/dl}

## Notes

`REASSIGN OWNED` is often used to prepare for the removal of one or more roles.
Because `REASSIGN OWNED` does not affect objects within other databases, it is usually necessary to execute this command in each database that contains objects owned by a role that is to be removed.

`REASSIGN OWNED` requires membership on both the source role(s) and the target role.

The [`DROP OWNED`](#sql-drop-owned) command is an alternative that simply drops all the database objects owned by one or more roles.

The `REASSIGN OWNED` command does not affect any privileges granted to the *old_roles* on objects that are not owned by them.
Likewise, it does not affect default privileges created with `ALTER DEFAULT PRIVILEGES`.
Use `DROP OWNED` to revoke such privileges.

See [Dropping Roles](braised:ref/role-removal) for more discussion.

## Compatibility

The `REASSIGN OWNED` command is a PostgreSQL extension.
