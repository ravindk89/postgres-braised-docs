---
title: "52.54. pg_subscription"
id: catalog-pg-subscription
---

## pg_subscription

The catalog pg_subscription contains all existing logical replication subscriptions.
For more information about logical replication see [Logical Replication](#logical-replication).

Unlike most system catalogs, pg_subscription is shared across all databases of a cluster: there is only one copy of pg_subscription per cluster, not one per database.

Access to the column subconninfo is revoked from normal users, because it could contain plain-text passwords.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subdbid `oid` (references [pg_database](#catalog-pg-database).oid)

   OID of the database that the subscription resides in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subskiplsn `pg_lsn`

   Finish LSN of the transaction whose changes are to be skipped, if a valid LSN; otherwise `0/0`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subname `name`

   Name of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the subscription
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subenabled `bool`

   If true, the subscription is enabled and should be replicating
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subbinary `bool`

   If true, the subscription will request that the publisher send data in binary format
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   substream `char`

   Controls how to handle the streaming of in-progress transactions: `f` = disallow streaming of in-progress transactions, `t` = spill the changes of in-progress transactions to disk and apply at once after the transaction is committed on the publisher and received by the subscriber, `p` = apply changes directly using a parallel apply worker if available (same as `t` if no worker is available)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subtwophasestate `char`

   State codes for two-phase mode: `d` = disabled, `p` = pending enablement, `e` = enabled
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subdisableonerr `bool`

   If true, the subscription will be disabled if one of its workers detects an error
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subpasswordrequired `bool`

   If true, the subscription will be required to specify a password for authentication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subrunasowner `bool`

   If true, the subscription will be run with the permissions of the subscription owner
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subfailover `bool`

   If true, the associated replication slots (i.e. the main slot and the table synchronization slots) in the upstream database are enabled to be synchronized to the standbys
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subconninfo `text`

   Connection string to the upstream database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subslotname `name`

   Name of the replication slot in the upstream database (also used for the local replication origin name); null represents `NONE`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subsynccommit `text`

   The `synchronous_commit` setting for the subscription\'s workers to use
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   subpublications `text[]`

   Array of subscribed publication names. These reference publications defined in the upstream database. For more on publications see [Publication](braised:ref/logical-replication-publication).
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   suborigin `text`

   The origin value must be either `none` or `any`. The default is `any`. If `none`, the subscription will request the publisher to only send changes that don\'t have an origin. If `any`, the publisher sends changes regardless of their origin.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_subscription Columns
