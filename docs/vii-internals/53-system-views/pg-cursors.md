---
title: "53.7. pg_cursors"
id: view-pg-cursors
---

## pg_cursors

The pg_cursors view lists the cursors that are currently available.
Cursors can be defined in several ways:

-   via the [`DECLARE`](#sql-declare) statement in SQL

-   via the Bind message in the frontend/backend protocol, as described in [Extended Query](braised:ref/protocol-flow#extended-query)

-   via the Server Programming Interface (SPI), as described in [Interface Functions](braised:ref/spi-interface)

The pg_cursors view displays cursors created by any of these means.
Cursors only exist for the duration of the transaction that defines them, unless they have been declared `WITH HOLD`.
Therefore non-holdable cursors are only present in the view until the end of their creating transaction.

:::{.callout type="note"}
Cursors are used internally to implement some of the components of PostgreSQL, such as procedural languages. Therefore, the pg_cursors view might include cursors that have not been explicitly created by the user.
:::

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   name `text`

   The name of the cursor
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   statement `text`

   The verbatim query string submitted to declare this cursor
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_holdable `bool`

   `true` if the cursor is holdable (that is, it can be accessed after the transaction that declared the cursor has committed); `false` otherwise
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_binary `bool`

   `true` if the cursor was declared `BINARY`; `false` otherwise
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   is_scrollable `bool`

   `true` if the cursor is scrollable (that is, it allows rows to be retrieved in a nonsequential manner); `false` otherwise
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   creation_time `timestamptz`

   The time at which the cursor was declared
  :::{/cell}
  :::{/row}
:::{/table}

: pg_cursors Columns

The pg_cursors view is read-only.
