---
title: "53.27. pg_shmem_allocations"
id: view-pg-shmem-allocations
---

## pg_shmem_allocations

The pg_shmem_allocations view shows allocations made from the server\'s main shared memory segment.
This includes both memory allocated by PostgreSQL itself and memory allocated by extensions using the mechanisms detailed in [Shared Memory](braised:ref/xfunc-c#shared-memory).

Note that this view does not include memory allocated using the dynamic shared memory infrastructure.

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

   The name of the shared memory allocation. NULL for unused memory and `<anonymous>` for anonymous allocations.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   off `int8`

   The offset at which the allocation starts. NULL for anonymous allocations, since details related to them are not known.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   size `int8`

   Size of the allocation in bytes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   allocated_size `int8`

   Size of the allocation in bytes including padding. For anonymous allocations, no information about padding is available, so the `size` and `allocated_size` columns will always be equal. Padding is not meaningful for free memory, so the columns will be equal in that case also.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_shmem_allocations Columns

Anonymous allocations are allocations that have been made with `ShmemAlloc()` directly, rather than via `ShmemInitStruct()` or `ShmemInitHash()`.

By default, the pg_shmem_allocations view can be read only by superusers or roles with privileges of the `pg_read_all_stats` role.
