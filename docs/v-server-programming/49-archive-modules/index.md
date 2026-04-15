---
title: 49. Archive Modules
id: archive-modules
---

PostgreSQL provides infrastructure to create custom modules for continuous archiving (see [Section 25.3](braised:ref/continuous-archiving)).
While archiving via a shell command (i.e., `archive_command`) is much simpler, a custom archive module will often be considerably more robust and performant.

When a custom `archive_library` is configured, PostgreSQL will submit completed WAL files to the module, and the server will avoid recycling or removing these WAL files until the module indicates that the files were successfully archived.
It is ultimately up to the module to decide what to do with each WAL file, but many recommendations are listed at [Section 25.3](braised:ref/continuous-archiving).

Archiving modules must at least consist of an initialization function (see [Section 49](braised:ref/archive-modules)) and the required callbacks (see [Section 49](braised:ref/archive-modules)).
However, archive modules are also permitted to do much more (e.g., declare GUCs and register background workers).

The `contrib/basic_archive` module contains a working example, which demonstrates some useful techniques.
