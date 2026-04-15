---
title: "53.20. pg_replication_slots"
id: view-pg-replication-slots
---

## pg_replication_slots

The pg_replication_slots view provides a listing of all replication slots that currently exist on the database cluster, along with their current state.

For more on replication slots, see [Replication Slots](braised:ref/warm-standby#replication-slots) and [Logical Decoding](#logical-decoding).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   slot_name `name`

   A unique, cluster-wide identifier for the replication slot
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   plugin `name`

   The base name of the shared object containing the output plugin this logical slot is using, or null for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   slot_type `text`

   The slot type: `physical` or `logical`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   datoid `oid` (references [pg_database](#catalog-pg-database).oid)

   The OID of the database this slot is associated with, or null. Only logical slots have an associated database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   database `name` (references [pg_database](#catalog-pg-database).datname)

   The name of the database this slot is associated with, or null. Only logical slots have an associated database.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   temporary `bool`

   True if this is a temporary replication slot. Temporary slots are not saved to disk and are automatically dropped on error or when the session has finished.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   active `bool`

   True if this slot is currently being streamed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   active_pid `int4`

   The process ID of the session streaming data for this slot. `NULL` if inactive.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   xmin `xid`

   The oldest transaction that this slot needs the database to retain. `VACUUM` cannot remove tuples deleted by any later transaction.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   catalog_xmin `xid`

   The oldest transaction affecting the system catalogs that this slot needs the database to retain. `VACUUM` cannot remove catalog tuples deleted by any later transaction.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   restart_lsn `pg_lsn`

   The address (`LSN`) of oldest WAL which still might be required by the consumer of this slot and thus won\'t be automatically removed during checkpoints unless this LSN gets behind more than [max_slot_wal_keep_size (integer)
       
        max_slot_wal_keep_size configuration parameter](braised:ref/runtime-config-replication#max-slot-wal-keep-size-integer-max-slot-wal-keep-size-configuration-parameter) from the current LSN. `NULL` if the `LSN` of this slot has never been reserved.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   confirmed_flush_lsn `pg_lsn`

   The address (`LSN`) up to which the logical slot\'s consumer has confirmed receiving data. Data corresponding to the transactions committed before this `LSN` is not available anymore. `NULL` for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   wal_status `text`

   Availability of WAL files claimed by this slot. Possible values are:

   -   `reserved` means that the claimed files are within `max_wal_size`.

   -   `extended` means that `max_wal_size` is exceeded but the files are still retained, either by the replication slot or by `wal_keep_size`.

   -   `unreserved` means that the slot no longer retains the required WAL files and some of them are to be removed at the next checkpoint. This typically occurs when [max_slot_wal_keep_size (integer)
       
        max_slot_wal_keep_size configuration parameter](braised:ref/runtime-config-replication#max-slot-wal-keep-size-integer-max-slot-wal-keep-size-configuration-parameter) is set to a non-negative value. This state can return to `reserved` or `extended`.

   -   `lost` means that this slot is no longer usable.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   safe_wal_size `int8`

   The number of bytes that can be written to WAL such that this slot is not in danger of getting in state \"lost\". It is NULL for lost slots, as well as if `max_slot_wal_keep_size` is `-1`.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   two_phase `bool`

   True if the slot is enabled for decoding prepared transactions. Always false for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   two_phase_at `pg_lsn`

   The address (`LSN`) from which the decoding of prepared transactions is enabled. `NULL` for logical slots where two_phase is false and for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   inactive_since `timestamptz`

   The time when the slot became inactive. `NULL` if the slot is currently being streamed. If the slot becomes invalid, this value will never be updated. For standby slots that are being synced from a primary server (whose synced field is `true`), the inactive_since indicates the time when slot synchronization (see [Replication Slot Synchronization](braised:ref/logicaldecoding-explanation#replication-slot-synchronization)) was most recently stopped. `NULL` if the slot has always been synchronized. This helps standby slots track when synchronization was interrupted.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   conflicting `bool`

   True if this logical slot conflicted with recovery (and so is now invalidated). When this column is true, check invalidation_reason column for the conflict reason. Always `NULL` for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   invalidation_reason `text`

   The reason for the slot\'s invalidation. It is set for both logical and physical slots. `NULL` if the slot is not invalidated. Possible values are:

   -   `wal_removed` means that the required WAL has been removed.
   -   `rows_removed` means that the required rows have been removed. It is set only for logical slots.
   -   `wal_level_insufficient` means that the primary doesn\'t have a [wal_level (enum)
      
       wal_level configuration parameter](braised:ref/runtime-config-wal#wal-level-enum-wal-level-configuration-parameter) sufficient to perform logical decoding. It is set only for logical slots.
   -   `idle_timeout` means that the slot has remained inactive longer than the configured [idle_replication_slot_timeout (integer)
      
       idle_replication_slot_timeout configuration parameter](braised:ref/runtime-config-replication#idle-replication-slot-timeout-integer-idle-replication-slot-timeout-configuration-parameter) duration.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   failover `bool`

   True if this is a logical slot enabled to be synced to the standbys so that logical replication can be resumed from the new primary after failover. Always false for physical slots.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   synced `bool`

   True if this is a logical slot that was synced from a primary server. On a hot standby, the slots with the synced column marked as true can neither be used for logical decoding nor dropped manually. The value of this column has no meaning on the primary server; the column value on the primary is default false for all slots but may (if leftover from a promoted standby) also be true.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_replication_slots Columns
