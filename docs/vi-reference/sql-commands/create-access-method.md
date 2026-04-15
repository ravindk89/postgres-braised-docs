---
title: "CREATE ACCESS METHOD"
layout: reference
id: sql-create-access-method
description: "define a new access method"
---

:::synopsis
CREATE ACCESS METHOD name
 TYPE access_method_type
 HANDLER handler_function
:::

## Description

`CREATE ACCESS METHOD` creates a new access method.

The access method name must be unique within the database.

Only superusers can define new access methods.

## Parameters

:::{.dl}
:::{.item term="*name*"}
The name of the access method to be created.
:::{/item}
:::{.item term="*access_method_type*"}
This clause specifies the type of access method to define. Only `TABLE` and `INDEX` are supported at present.
:::{/item}
:::{.item term="*handler_function*"}
*handler_function* is the name (possibly schema-qualified) of a previously registered function that represents the access method. The handler function must be declared to take a single argument of type `internal`, and its return type depends on the type of access method; for `TABLE` access methods, it must be `table_am_handler` and for `INDEX` access methods, it must be `index_am_handler`. The C-level API that the handler function must implement varies depending on the type of access method. The table access method API is described in [Table Access Method Interface Definition](braised:ref/tableam) and the index access method API is described in [Index Access Method Interface Definition](#index-access-method-interface-definition).
:::{/item}
:::{/dl}

## Examples

Create an index access method `heptree` with handler function `heptree_handler`:

    CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;

## Compatibility

`CREATE ACCESS METHOD` is a PostgreSQL extension.
