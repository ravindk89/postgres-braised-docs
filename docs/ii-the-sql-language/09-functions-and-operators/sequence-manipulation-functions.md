---
title: "9.17. Sequence Manipulation Functions"
id: functions-sequence
---

## Sequence Manipulation Functions

This section describes functions for operating on sequence objects, also called sequence generators or just sequences.
Sequence objects are special single-row tables created with [CREATE SEQUENCE](braised:ref/sql-createsequence).
Sequence objects are commonly used to generate unique identifiers for rows of a table.
The sequence functions, listed in Sequence Functions, provide simple, multiuser-safe methods for obtaining successive sequence values from sequence objects.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `nextval` ( `regclass` ) bigint

   Advances the sequence object to its next value and returns that value. This is done atomically: even if multiple sessions execute `nextval` concurrently, each will safely receive a distinct sequence value. If the sequence object has been created with default parameters, successive `nextval` calls will return successive values beginning with 1. Other behaviors can be obtained by using appropriate parameters in the [CREATE SEQUENCE](braised:ref/sql-createsequence) command.

   This function requires `USAGE` or `UPDATE` privilege on the sequence.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `setval` ( `regclass`, `bigint` \[, `boolean`\] ) bigint

   Sets the sequence object\'s current value, and optionally its `is_called` flag. The two-parameter form sets the sequence\'s `last_value` field to the specified value and sets its `is_called` field to `true`, meaning that the next `nextval` will advance the sequence before returning a value. The value that will be reported by `currval` is also set to the specified value. In the three-parameter form, `is_called` can be set to either `true` or `false`. `true` has the same effect as the two-parameter form. If it is set to `false`, the next `nextval` will return exactly the specified value, and sequence advancement commences with the following `nextval`. Furthermore, the value reported by `currval` is not changed in this case. For example,

       SELECT setval('myseq', 42);           Next nextval will return 43
       SELECT setval('myseq', 42, true);     Same as above
       SELECT setval('myseq', 42, false);    Next nextval will return 42

   The result returned by `setval` is just the value of its second argument.

   This function requires `UPDATE` privilege on the sequence.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `currval` ( `regclass` ) bigint

   Returns the value most recently obtained by `nextval` for this sequence in the current session. (An error is reported if `nextval` has never been called for this sequence in this session.) Because this is returning a session-local value, it gives a predictable answer whether or not other sessions have executed `nextval` since the current session did.

   This function requires `USAGE` or `SELECT` privilege on the sequence.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lastval` () bigint

   Returns the value most recently returned by `nextval` in the current session. This function is identical to `currval`, except that instead of taking the sequence name as an argument it refers to whichever sequence `nextval` was most recently applied to in the current session. It is an error to call `lastval` if `nextval` has not yet been called in the current session.

   This function requires `USAGE` or `SELECT` privilege on the last used sequence.
  :::{/cell}
  :::{/row}
:::{/table}

: Sequence Functions

:::{.callout type="caution"}
To avoid blocking concurrent transactions that obtain numbers from the same sequence, the value obtained by `nextval` is not reclaimed for re-use if the calling transaction later aborts. This means that transaction aborts or database crashes can result in gaps in the sequence of assigned values. That can happen without a transaction abort, too. For example an `INSERT` with an `ON CONFLICT` clause will compute the to-be-inserted tuple, including doing any required `nextval` calls, before detecting any conflict that would cause it to follow the `ON CONFLICT` rule instead. Thus, PostgreSQL sequence objects *cannot be used to obtain "gapless" sequences*.

Likewise, sequence state changes made by `setval` are immediately visible to other transactions, and are not undone if the calling transaction rolls back.

If the database cluster crashes before committing a transaction containing a `nextval` or `setval` call, the sequence state change might not have made its way to persistent storage, so that it is uncertain whether the sequence will have its original or updated state after the cluster restarts. This is harmless for usage of the sequence within the database, since other effects of uncommitted transactions will not be visible either. However, if you wish to use a sequence value for persistent outside-the-database purposes, make sure that the `nextval` call has been committed before doing so.
:::

The sequence to be operated on by a sequence function is specified by a `regclass` argument, which is simply the OID of the sequence in the pg_class system catalog.
You do not have to look up the OID by hand, however, since the `regclass` data type\'s input converter will do the work for you.
See [Object Identifier Types](braised:ref/datatype-oid) for details.
