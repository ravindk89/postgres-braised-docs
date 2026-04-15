---
title: F. Additional Supplied Modules and Extensions
id: contrib
---

This appendix and the next one contain information on the optional components found in the `contrib` directory of the PostgreSQL distribution.
These include porting tools, analysis utilities, and plug-in features that are not part of the core PostgreSQL system.
They are separate mainly because they address a limited audience or are too experimental to be part of the main source tree.
This does not preclude their usefulness.

This appendix covers extensions and other server plug-in module libraries found in `contrib`. [G. Additional Supplied Programs](braised:ref/contrib-prog) covers utility programs.

When building from the source distribution, these optional components are not built automatically, unless you build the \"world\" target (see [Section 17.3](braised:ref/install-make)).
You can build and install all of them by running:

    make
    make install

in the `contrib` directory of a configured source tree; or to build and install just one selected module, do the same in that module\'s subdirectory.
Many of the modules have regression tests, which can be executed by running:

    make check

before installation or

    make installcheck

once you have a PostgreSQL server running.

If you are using a pre-packaged version of PostgreSQL, these components are typically made available as a separate subpackage, such as `postgresql-contrib`.

Many components supply new user-defined functions, operators, or types, packaged as extensions.
To make use of one of these extensions, after you have installed the code you need to register the new SQL objects in the database system.
This is done by executing a [CREATE EXTENSION](braised:ref/sql-createextension) command.
In a fresh database, you can simply do

    CREATE EXTENSION extension_name;

This command registers the new SQL objects in the current database only, so you need to run it in every database in which you want the extension\'s facilities to be available.
Alternatively, run it in database `template1` so that the extension will be copied into subsequently-created databases by default.

For all extensions, the `CREATE EXTENSION` command must be run by a database superuser, unless the extension is considered "trusted".
Trusted extensions can be run by any user who has `CREATE` privilege on the current database.
Extensions that are trusted are identified as such in the sections that follow.
Generally, trusted extensions are ones that cannot provide access to outside-the-database functionality.

The following extensions are trusted in a default installation: [btree_gin](braised:ref/btree-gin), [btree_gist](braised:ref/btree-gist), [citext](braised:ref/citext), [cube](braised:ref/cube), [dict_int](braised:ref/dict-int), [fuzzystrmatch](braised:ref/fuzzystrmatch), [hstore](braised:ref/hstore), [intarray](braised:ref/intarray), [isn](braised:ref/isn), [lo](braised:ref/lo), [ltree](braised:ref/ltree), [pgcrypto](braised:ref/pgcrypto), [pg_trgm](braised:ref/pgtrgm), [seg](braised:ref/seg), [tablefunc](braised:ref/tablefunc), [tcn](braised:ref/tcn), [tsm_system_rows](braised:ref/tsm-system-rows), [tsm_system_time](braised:ref/tsm-system-time), [unaccent](braised:ref/unaccent), [uuid-ossp](braised:ref/uuid-ossp)

Many extensions allow you to install their objects in a schema of your choice.
To do that, add `SCHEMA schema_name` to the `CREATE EXTENSION` command.
By default, the objects will be placed in your current creation target schema, which in turn defaults to `public`.

Note, however, that some of these components are not "extensions" in this sense, but are loaded into the server in some other way, for instance by way of `shared_preload_libraries`.
See the documentation of each component for details.
