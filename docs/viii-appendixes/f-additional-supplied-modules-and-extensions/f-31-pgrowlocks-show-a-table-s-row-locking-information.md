---
title: "F.31. pgrowlocks — show a table's row locking information"
id: pgrowlocks
---

## pgrowlocks show a table\'s row locking information

The `pgrowlocks` module provides a function to show row locking information for a specified table.

By default use is restricted to superusers, roles with privileges of the `pg_stat_scan_tables` role, and users with `SELECT` permissions on the table.

### Overview

pgrowlocks(text) returns setof record

The parameter is the name of a table.
The result is a set of records, with one row for each locked row within the table.
The output columns are shown in [Output Columns](#pgrowlocks-columns).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Type
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  locked_row
  :::{/cell}
  :::{.cell}
  `tid`
  :::{/cell}
  :::{.cell}
  Tuple ID (TID) of locked row
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  locker
  :::{/cell}
  :::{.cell}
  `xid`
  :::{/cell}
  :::{.cell}
  Transaction ID of locker, or multixact ID if multitransaction; see [Transactions and Identifiers](braised:ref/transaction-id)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  multi
  :::{/cell}
  :::{.cell}
  `boolean`
  :::{/cell}
  :::{.cell}
  True if locker is a multitransaction
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  xids
  :::{/cell}
  :::{.cell}
  `xid[]`
  :::{/cell}
  :::{.cell}
  Transaction IDs of lockers (more than one if multitransaction)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  modes
  :::{/cell}
  :::{.cell}
  `text[]`
  :::{/cell}
  :::{.cell}
  Lock mode of lockers (more than one if multitransaction), an array of `For Key Share`, `For Share`, `For No Key Update`, `No Key Update`, `For Update`, `Update`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pids
  :::{/cell}
  :::{.cell}
  `integer[]`
  :::{/cell}
  :::{.cell}
  Process IDs of locking backends (more than one if multitransaction)
  :::{/cell}
  :::{/row}
:::{/table}

  : `pgrowlocks` Output Columns

`pgrowlocks` takes `AccessShareLock` for the target table and reads each row one by one to collect the row locking information. This is not very speedy for a large table. Note that:

1.  If an `ACCESS EXCLUSIVE` lock is taken on the table, `pgrowlocks` will be blocked.

2.  `pgrowlocks` is not guaranteed to produce a self-consistent snapshot. It is possible that a new row lock is taken, or an old lock is freed, during its execution.

`pgrowlocks` does not show the contents of locked rows. If you want to take a look at the row contents at the same time, you could do something like this:

    SELECT * FROM accounts AS a, pgrowlocks('accounts') AS p
      WHERE p.locked_row = a.ctid;

Be aware however that such a query will be very inefficient.

### Sample Output

    =# SELECT * FROM pgrowlocks('t1');
     locked_row | locker | multi | xids  |     modes      |  pids
    ------------+--------+-------+-------+----------------+--------
     (0,1)      |    609 | f     | {609} | {"For Share"}  | {3161}
     (0,2)      |    609 | f     | {609} | {"For Share"}  | {3161}
     (0,3)      |    607 | f     | {607} | {"For Update"} | {3107}
     (0,4)      |    607 | f     | {607} | {"For Update"} | {3107}
    (4 rows)

### Author

Tatsuo Ishii
