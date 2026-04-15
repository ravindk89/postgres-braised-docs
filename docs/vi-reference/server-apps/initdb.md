---
title: "initdb"
layout: reference
id: app-initdb
description: "create a new PostgreSQL database cluster"
---

:::synopsis
initdb
 option
 
 
 --pgdata
 -D
 
 directory
:::

## Description

## Description

`initdb` creates a new PostgreSQL database cluster.

Creating a database cluster consists of creating the directories in which the cluster data will live, generating the shared catalog tables (tables that belong to the whole cluster rather than to any particular database), and creating the `postgres`, `template1`, and `template0` databases.
The `postgres` database is a default database meant for use by users, utilities and third party applications. `template1` and `template0` are meant as source databases to be copied by later `CREATE DATABASE` commands. `template0` should never be modified, but you can add objects to `template1`, which by default will be copied into databases created later.
See [Template Databases](braised:ref/manage-ag-templatedbs) for more details.

Although `initdb` will attempt to create the specified data directory, it might not have permission if the parent directory of the desired data directory is root-owned.
To initialize in such a setup, create an empty data directory as root, then use `chown` to assign ownership of that directory to the database user account, then `su` to become the database user to run `initdb`.

`initdb` must be run as the user that will own the server process, because the server needs to have access to the files and directories that `initdb` creates.
Since the server cannot be run as root, you must not run `initdb` as root either. (It will in fact refuse to do so.)

For security reasons the new cluster created by `initdb` will only be accessible by the cluster owner by default.
The `--allow-group-access` option allows any user in the same group as the cluster owner to read files in the cluster.
This is useful for performing backups as a non-privileged user.

`initdb` initializes the database cluster\'s default locale and character set encoding.
These can also be set separately for each database when it is created. `initdb` determines those settings for the template databases, which will serve as the default for all other databases.

By default, `initdb` uses the locale provider `libc` (see [Locale Providers](braised:ref/locale#locale-providers)).
The `libc` locale provider takes the locale settings from the environment, and determines the encoding from the locale settings.

To choose a different locale for the cluster, use the option `--locale`.
There are also individual options `--lc-*` and `--icu-locale` (see below) to set values for the individual locale categories.
Note that inconsistent settings for different locale categories can give nonsensical results, so this should be used with care.

Alternatively, `initdb` can use the ICU library to provide locale services by specifying `--locale-provider=icu`.
The server must be built with ICU support.
To choose the specific ICU locale ID to apply, use the option `--icu-locale`.
Note that for implementation reasons and to support legacy code, `initdb` will still select and initialize libc locale settings when the ICU locale provider is used.

When `initdb` runs, it will print out the locale settings it has chosen.
If you have complex requirements or specified multiple options, it is advisable to check that the result matches what was intended.

More details about locale settings can be found in [Locale Support](braised:ref/locale).

To alter the default encoding, use the `--encoding`.
More details can be found in [Character Set Support](braised:ref/multibyte).

## Options

:::{.dl}
:::{.item term="`-A authmethod`; `--auth=authmethod`"}
This option specifies the default authentication method for local users used in `pg_hba.conf` (`host` and `local` lines). See [The pg_hba.conf File](braised:ref/auth-pg-hba-conf) for an overview of valid values.

`initdb` will prepopulate `pg_hba.conf` entries using the specified authentication method for non-replication as well as replication connections.

Do not use `trust` unless you trust all local users on your system. `trust` is the default for ease of installation.
:::{/item}
:::{.item term="`--auth-host=authmethod`"}
This option specifies the authentication method for local users via TCP/IP connections used in `pg_hba.conf` (`host` lines).
:::{/item}
:::{.item term="`--auth-local=authmethod`"}
This option specifies the authentication method for local users via Unix-domain socket connections used in `pg_hba.conf` (`local` lines).
:::{/item}
:::{.item term="`-D directory`; `--pgdata=directory`"}
This option specifies the directory where the database cluster should be stored. This is the only information required by `initdb`, but you can avoid writing it by setting the `PGDATA` environment variable, which can be convenient since the database server (`postgres`) can find the data directory later by the same variable.
:::{/item}
:::{.item term="`-E encoding`; `--encoding=encoding`"}
Selects the encoding of the template databases. This will also be the default encoding of any database you create later, unless you override it then. The character sets supported by the PostgreSQL server are described in [Supported Character Sets](braised:ref/multibyte#supported-character-sets).

By default, the template database encoding is derived from the locale. If `--no-locale` is specified (or equivalently, if the locale is `C` or `POSIX`), then the default is `UTF8` for the ICU provider and `SQL_ASCII` for the `libc` provider.
:::{/item}
:::{.item term="`-g`; `--allow-group-access`"}
Allows users in the same group as the cluster owner to read all cluster files created by `initdb`. This option is ignored on Windows as it does not support POSIX-style group permissions.
:::{/item}
:::{.item term="`--icu-locale=locale`"}
Specifies the ICU locale when the ICU provider is used. Locale support is described in [Locale Support](braised:ref/locale).
:::{/item}
:::{.item term="`--icu-rules=rules`"}
Specifies additional collation rules to customize the behavior of the default collation. This is supported for ICU only.
:::{/item}
:::{.item term="`-k`; `--data-checksums`"}
Use checksums on data pages to help detect corruption by the I/O system that would otherwise be silent. This is enabled by default; use `app-initdb-no-data-checksums` to disable checksums.

Enabling checksums might incur a small performance penalty. If set, checksums are calculated for all objects, in all databases. All checksum failures will be reported in the [pg_stat_database](#monitoring-pg-stat-database-view) view. See [Data Checksums](braised:ref/checksums) for details.
:::{/item}
:::{.item term="`--locale=locale`"}
Sets the default locale for the database cluster. If this option is not specified, the locale is inherited from the environment that `initdb` runs in. Locale support is described in [Locale Support](braised:ref/locale).

If `--locale-provider` is `builtin`, `--locale` or `--builtin-locale` must be specified and set to `C`, `C.UTF-8` or `PG_UNICODE_FAST`.
:::{/item}
:::{.item term="`--lc-collate=locale`; `--lc-ctype=locale`; `--lc-messages=locale`; `--lc-monetary=locale`; `--lc-numeric=locale`; `--lc-time=locale`"}
Like `--locale`, but only sets the locale in the specified category.
:::{/item}
:::{.item term="`--no-locale`"}
Equivalent to `--locale=C`.
:::{/item}
:::{.item term="`--builtin-locale=locale`"}
Specifies the locale name when the builtin provider is used. Locale support is described in [Locale Support](braised:ref/locale).
:::{/item}
:::{.item term="`--locale-provider={builtin|libc|icu}`"}
This option sets the locale provider for databases created in the new cluster. It can be overridden in the `CREATE DATABASE` command when new databases are subsequently created. The default is `libc` (see [Locale Providers](braised:ref/locale#locale-providers)).
:::{/item}
:::{.item term="`--no-data-checksums`"}
Do not enable data checksums.
:::{/item}
:::{.item term="`--pwfile=filename`"}
Makes `initdb` read the bootstrap superuser\'s password from a file. The first line of the file is taken as the password.
:::{/item}
:::{.item term="`-T config`; `--text-search-config=config`"}
Sets the default text search configuration. See [default_text_search_config (string)
      
   default_text_search_config configuration parameter](braised:ref/runtime-config-client#default-text-search-config-string-default-text-search-config-configuration-parameter) for further information.
:::{/item}
:::{.item term="`-U username`; `--username=username`"}
Sets the user name of the bootstrap superuser. This defaults to the name of the operating-system user running `initdb`.
:::{/item}
:::{.item term="`-W`; `--pwprompt`"}
Makes `initdb` prompt for a password to give the bootstrap superuser. If you don\'t plan on using password authentication, this is not important. Otherwise you won\'t be able to use password authentication until you have a password set up.
:::{/item}
:::{.item term="`-X directory`; `--waldir=directory`"}
This option specifies the directory where the write-ahead log should be stored.
:::{/item}
:::{.item term="`--wal-segsize=size`"}
Set the WAL segment size, in megabytes. This is the size of each individual file in the WAL log. The default size is 16 megabytes. The value must be a power of 2 between 1 and 1024 (megabytes). This option can only be set during initialization, and cannot be changed later.

It may be useful to adjust this size to control the granularity of WAL log shipping or archiving. Also, in databases with a high volume of WAL, the sheer number of WAL files per directory can become a performance and management problem. Increasing the WAL file size will reduce the number of WAL files.
:::{/item}
:::{/dl}

Other, less commonly used, options are also available:

:::{.dl}
:::{.item term="`-c name=value`; `--set name=value`"}
Forcibly set the server parameter *name* to *value* during `initdb`, and also install that setting in the generated `postgresql.conf` file, so that it will apply during future server runs. This option can be given more than once to set several parameters. It is primarily useful when the environment is such that the server will not start at all using the default parameters.
:::{/item}
:::{.item term="`-d`; `--debug`"}
Print debugging output from the bootstrap backend and a few other messages of lesser interest for the general public. The bootstrap backend is the program `initdb` uses to create the catalog tables. This option generates a tremendous amount of extremely boring output.
:::{/item}
:::{.item term="`--discard-caches`"}
Run the bootstrap backend with the `debug_discard_caches=1` option. This takes a very long time and is only of use for deep debugging.
:::{/item}
:::{.item term="`-L directory`"}
Specifies where `initdb` should find its input files to initialize the database cluster. This is normally not necessary. You will be told if you need to specify their location explicitly.
:::{/item}
:::{.item term="`-n`; `--no-clean`"}
By default, when `initdb` determines that an error prevented it from completely creating the database cluster, it removes any files it might have created before discovering that it cannot finish the job. This option inhibits tidying-up and is thus useful for debugging.
:::{/item}
:::{.item term="`-N`; `--no-sync`"}
By default, `initdb` will wait for all files to be written safely to disk. This option causes `initdb` to return without waiting, which is faster, but means that a subsequent operating system crash can leave the data directory corrupt. Generally, this option is useful for testing, but should not be used when creating a production installation.
:::{/item}
:::{.item term="`--no-sync-data-files`"}
By default, `initdb` safely writes all database files to disk. This option instructs `initdb` to skip synchronizing all files in the individual database directories, the database directories themselves, and the tablespace directories, i.e., everything in the `base` subdirectory and any other tablespace directories. Other files, such as those in `pg_wal` and `pg_xact`, will still be synchronized unless the `--no-sync` option is also specified.

Note that if `--no-sync-data-files` is used in conjunction with `--sync-method=syncfs`, some or all of the aforementioned files and directories will be synchronized because `syncfs` processes entire file systems.

This option is primarily intended for internal use by tools that separately ensure the skipped files are synchronized to disk.
:::{/item}
:::{.item term="`--no-instructions`"}
By default, `initdb` will write instructions for how to start the cluster at the end of its output. This option causes those instructions to be left out. This is primarily intended for use by tools that wrap `initdb` in platform-specific behavior, where those instructions are likely to be incorrect.
:::{/item}
:::{.item term="`-s`; `--show`"}
Show internal settings and exit, without doing anything else. This can be used to debug the initdb installation.
:::{/item}
:::{.item term="`--sync-method=method`"}
When set to `fsync`, which is the default, `initdb` will recursively open and synchronize all files in the data directory. The search for files will follow symbolic links for the WAL directory and each configured tablespace.

On Linux, `syncfs` may be used instead to ask the operating system to synchronize the whole file systems that contain the data directory, the WAL files, and each tablespace. See [recovery_init_sync_method (enum)
       
    recovery_init_sync_method configuration parameter](braised:ref/runtime-config-error-handling#recovery-init-sync-method-enum-recovery-init-sync-method-configuration-parameter) for information about the caveats to be aware of when using `syncfs`.

This option has no effect when `--no-sync` is used.
:::{/item}
:::{.item term="`-S`; `--sync-only`"}
Safely write all database files to disk and exit. This does not perform any of the normal initdb operations. Generally, this option is useful for ensuring reliable recovery after changing [fsync (boolean)
      
   fsync configuration parameter](braised:ref/runtime-config-wal#fsync-boolean-fsync-configuration-parameter) from `off` to `on`.
:::{/item}
:::{/dl}

Other options:

:::{.dl}
:::{.item term="`-V`; `--version`"}
Print the initdb version and exit.
:::{/item}
:::{.item term="`-?`; `--help`"}
Show help about initdb command line arguments, and exit.
:::{/item}
:::{/dl}

## Environment

:::{.dl}
:::{.item term="`PGDATA`"}
Specifies the directory where the database cluster is to be stored; can be overridden using the `-D` option.
:::{/item}
:::{.item term="`PG_COLOR`"}
Specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.
:::{/item}
:::{.item term="`TZ`"}
Specifies the default time zone of the created database cluster. The value should be a full time zone name (see [Time Zones](braised:ref/datatype-datetime#time-zones)).
:::{/item}
:::{/dl}

## Notes

`initdb` can also be invoked via `pg_ctl initdb`.
