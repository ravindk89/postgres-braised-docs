---
title: "53.2. pg_aios"
id: view-pg-aios
---

## pg_aios

The pg_aios view lists all [glossary-aio](braised:ref/glossary#glossary-aio) handles that are currently in-use.
An I/O handle is used to reference an I/O operation that is being prepared, executed or is in the process of completing. pg_aios contains one row for each I/O handle.

This view is mainly useful for developers of PostgreSQL, but may also be useful when tuning PostgreSQL.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pid `int4`

   Process ID of the server process that is issuing this I/O.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   io_id `int4`

   Identifier of the I/O handle. Handles are reused once the I/O completed (or if the handle is released before I/O is started). On reuse [pg_aios.io_generation ](#view-pg-aios-io-generation) is incremented.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   io_generation `int8`

   Generation of the I/O handle.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   state `text`

   State of the I/O handle:

   -   `HANDED_OUT`, referenced by code but not yet used

   -   `DEFINED`, information necessary for execution is known

   -   `STAGED`, ready for execution

   -   `SUBMITTED`, submitted for execution

   -   `COMPLETED_IO`, finished, but result has not yet been processed

   -   `COMPLETED_SHARED`, shared completion processing completed

   -   `COMPLETED_LOCAL`, backend local completion processing completed
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   operation `text`

   Operation performed using the I/O handle:

   -   `invalid`, not yet known

   -   `readv`, a vectored read

   -   `writev`, a vectored write
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   off `int8`

   Offset of the I/O operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   length `int8`

   Length of the I/O operation.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   target `text`

   What kind of object is the I/O targeting:

   -   `smgr`, I/O on relations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   handle_data_len `int2`

   Length of the data associated with the I/O operation. For I/O to/from [shared_buffers (integer)
      
       shared_buffers configuration parameter](braised:ref/runtime-config-resource#shared-buffers-integer-shared-buffers-configuration-parameter) and [temp_buffers (integer)
      
       temp_buffers configuration parameter](braised:ref/runtime-config-resource#temp-buffers-integer-temp-buffers-configuration-parameter), this indicates the number of buffers the I/O is operating on.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   raw_result `int4`

   Low-level result of the I/O operation, or NULL if the operation has not yet completed.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   result `text`

   High-level result of the I/O operation:

   -   `UNKNOWN` means that the result of the operation is not yet known.

   -   `OK` means the I/O completed successfully.

   -   `PARTIAL` means that the I/O completed without error, but did not process all data. Commonly callers will need to retry and perform the remainder of the work in a separate I/O.

   -   `WARNING` means that the I/O completed without error, but that execution of the IO triggered a warning. E.g. when encountering a corrupted buffer with [zero_damaged_pages (boolean)
      
       zero_damaged_pages configuration parameter](braised:ref/runtime-config-developer#zero-damaged-pages-boolean-zero-damaged-pages-configuration-parameter) enabled.

   -   `ERROR` means the I/O failed with an error.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   target_desc `text`

   Description of what the I/O operation is targeting.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   f_sync `bool`

   Flag indicating whether the I/O is executed synchronously.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   f_localmem `bool`

   Flag indicating whether the I/O references process local memory.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   f_buffered `bool`

   Flag indicating whether the I/O is buffered I/O.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_aios Columns

The pg_aios view is read-only.

By default, the pg_aios view can be read only by superusers or roles with privileges of the `pg_read_all_stats` role.
