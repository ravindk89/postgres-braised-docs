---
title: "53.5. pg_backend_memory_contexts"
id: view-pg-backend-memory-contexts
---

## pg_backend_memory_contexts

The view pg_backend_memory_contexts displays all the memory contexts of the server process attached to the current session.

pg_backend_memory_contexts contains one row for each memory context.

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

   Name of the memory context
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   ident `text`

   Identification information of the memory context. This field is truncated at 1024 bytes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   type `text`

   Type of the memory context
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   level `int4`

   The 1-based level of the context in the memory context hierarchy. The level of a context also shows the position of that context in the path column.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   path `int4[]`

   Array of transient numerical identifiers to describe the memory context hierarchy. The first element is for `TopMemoryContext`, subsequent elements contain intermediate parents and the final element contains the identifier for the current context.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_bytes `int8`

   Total bytes allocated for this memory context
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   total_nblocks `int8`

   Total number of blocks allocated for this memory context
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   free_bytes `int8`

   Free space in bytes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   free_chunks `int8`

   Total number of free chunks
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   used_bytes `int8`

   Used space in bytes
  :::{/cell}
  :::{/row}
:::{/table}

: pg_backend_memory_contexts Columns

By default, the pg_backend_memory_contexts view can be read only by superusers or roles with the privileges of the `pg_read_all_stats` role.

Since memory contexts are created and destroyed during the running of a query, the identifiers stored in the path column can be unstable between multiple invocations of the view in the same query. The example below demonstrates an effective usage of this column and calculates the total number of bytes used by `CacheMemoryContext` and all of its children:

    WITH memory_contexts AS (
        SELECT * FROM pg_backend_memory_contexts
    )
    SELECT sum(c1.total_bytes)
    FROM memory_contexts c1, memory_contexts c2
    WHERE c2.name = 'CacheMemoryContext'
    AND c1.path[c2.level] = c2.path[c2.level];

The [Common Table Expression](#queries-with) is used to ensure the context IDs in the path column match between both evaluations of the view.
