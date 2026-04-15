---
title: "vacuumdb"
layout: reference
id: app-vacuumdb
description: "garbage-collect and analyze a PostgreSQL database"
---

:::synopsis
vacuumdb
 connection-option
 option

 
 
 
 -t
 --table
 
 table
 ( column [,...] )
 
 

 
 
 dbname
 -a
 --all
vacuumdb
 connection-option
 option

 
 
 
 -n
 --schema
 
 schema
 
 

 
 
 dbname
 -a
 --all
vacuumdb
 connection-option
 option

 
 
 
 -N
 --exclude-schema
 
 schema
 
 

 
 
 dbname
 -a
 --all
:::

## Description

vacuumdb is a utility for cleaning a PostgreSQL database. vacuumdb will also generate internal statistics used by the PostgreSQL query optimizer.

vacuumdb is a wrapper around the SQL command [`VACUUM`](#sql-vacuum).
There is no effective difference between vacuuming and analyzing databases via this utility and via other methods for accessing the server.

## Options

vacuumdb accepts the following command-line arguments:

:::{.dl}
:::{.item term="`-a`; `--all`"}
Vacuum all databases.
:::{/item}
:::{.item term="`--buffer-usage-limit size`"}
Specifies the Buffer Access Strategy ring buffer size for a given invocation of vacuumdb. This size is used to calculate the number of shared buffers which will be reused as part of this strategy. See [VACUUM](braised:ref/sql-vacuum).
:::{/item}
:::{.item term="`-d dbname`; `--dbname=dbname`"}
Specifies the name of the database to be cleaned or analyzed, when `-a`/`--all` is not used. If this is not specified, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used. The *dbname* can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options.
:::{/item}
:::{.item term="`--disable-page-skipping`"}
Disable skipping pages based on the contents of the visibility map.
:::{/item}
:::{.item term="`-e`; `--echo`"}
Echo the commands that vacuumdb generates and sends to the server.
:::{/item}
:::{.item term="`-f`; `--full`"}
Perform "full" vacuuming.
:::{/item}
:::{.item term="`-F`; `--freeze`"}
Aggressively "freeze" tuples.
:::{/item}
:::{.item term="`--force-index-cleanup`"}
Always remove index entries pointing to dead tuples.
:::{/item}
:::{.item term="`-j njobs`; `--jobs=njobs`"}
Execute the vacuum or analyze commands in parallel by running *njobs* commands simultaneously. This option may reduce the processing time but it also increases the load on the database server.

vacuumdb will open *njobs* connections to the database, so make sure your [max_connections (integer)
      
   max_connections configuration parameter](braised:ref/runtime-config-connection#max-connections-integer-max-connections-configuration-parameter) setting is high enough to accommodate all connections.

Note that using this mode together with the `-f` (`FULL`) option might cause deadlock failures if certain system catalogs are processed in parallel.
:::{/item}
:::{.item term="`--min-mxid-age mxid_age`"}
Only execute the vacuum or analyze commands on tables with a multixact ID age of at least *mxid_age*. This setting is useful for prioritizing tables to process to prevent multixact ID wraparound (see [Multixacts and Wraparound](braised:ref/routine-vacuuming#multixacts-and-wraparound)).

For the purposes of this option, the multixact ID age of a relation is the greatest of the ages of the main relation and its associated TOAST table, if one exists. Since the commands issued by vacuumdb will also process the TOAST table for the relation if necessary, it does not need to be considered separately.
:::{/item}
:::{.item term="`--min-xid-age xid_age`"}
Only execute the vacuum or analyze commands on tables with a transaction ID age of at least *xid_age*. This setting is useful for prioritizing tables to process to prevent transaction ID wraparound (see [Preventing Transaction ID Wraparound Failures](braised:ref/routine-vacuuming#preventing-transaction-id-wraparound-failures)).

For the purposes of this option, the transaction ID age of a relation is the greatest of the ages of the main relation and its associated TOAST table, if one exists. Since the commands issued by vacuumdb will also process the TOAST table for the relation if necessary, it does not need to be considered separately.
:::{/item}
:::{.item term="`--missing-stats-only`"}
Only analyze relations that are missing statistics for a column, index expression, or extended statistics object. When used with `--analyze-in-stages`, this option prevents vacuumdb from temporarily replacing existing statistics with ones generated with lower statistics targets, thus avoiding transiently worse query optimizer choices.

This option can only be used in conjunction with `--analyze-only` or `--analyze-in-stages`.

Note that `--missing-stats-only` requires `SELECT` privileges on [pg_statistic](#catalog-pg-statistic) and [pg_statistic_ext_data](#catalog-pg-statistic-ext-data), which are restricted to superusers by default.
:::{/item}
:::{.item term="`-n schema`; `--schema=schema`"}
Clean or analyze all tables in *schema* only. Multiple schemas can be vacuumed by writing multiple `-n` switches.
:::{/item}
:::{.item term="`-N schema`; `--exclude-schema=schema`"}
Do not clean or analyze any tables in *schema*. Multiple schemas can be excluded by writing multiple `-N` switches.
:::{/item}
:::{.item term="`--no-index-cleanup`"}
Do not remove index entries pointing to dead tuples.
:::{/item}
:::{.item term="`--no-process-main`"}
Skip the main relation.
:::{/item}
:::{.item term="`--no-process-toast`"}
Skip the TOAST table associated with the table to vacuum, if any.
:::{/item}
:::{.item term="`--no-truncate`"}
Do not truncate empty pages at the end of the table.
:::{/item}
:::{.item term="`-P parallel_workers`; `--parallel=parallel_workers`"}
Specify the number of parallel workers for parallel vacuum. This allows the vacuum to leverage multiple CPUs to process indexes. See [VACUUM](braised:ref/sql-vacuum).
:::{/item}
:::{.item term="`-q`; `--quiet`"}
Do not display progress messages.
:::{/item}
:::{.item term="`--skip-locked`"}
Skip relations that cannot be immediately locked for processing.
:::{/item}
:::{.item term="`-t table [ (column [,...]) ]`; `--table=table [ (column [,...]) ]`"}
Clean or analyze *table* only. Column names can be specified only in conjunction with the `--analyze` or `--analyze-only` options. Multiple tables can be vacuumed by writing multiple `-t` switches.

:::{.callout type="tip"}
If you specify columns, you probably have to escape the parentheses from the shell. (See examples below.)
:::
:::{/item}
:::{.item term="`-v`; `--verbose`"}
Print detailed information during processing.
:::{/item}
:::{.item term="`-V`; `--version`"}
Print the vacuumdb version and exit.
:::{/item}
:::{.item term="`-z`; `--analyze`"}
Also calculate statistics for use by the optimizer.
:::{/item}
:::{.item term="`-Z`; `--analyze-only`"}
Only calculate statistics for use by the optimizer (no vacuum).
:::{/item}
:::{.item term="`--analyze-in-stages`"}
Only calculate statistics for use by the optimizer (no vacuum), like `--analyze-only`. Run three stages of analyze; the first stage uses the lowest possible statistics target (see [default_statistics_target (integer)
      
   default_statistics_target configuration parameter](braised:ref/runtime-config-query#default-statistics-target-integer-default-statistics-target-configuration-parameter)) to produce usable statistics faster, and subsequent stages build the full statistics.

This option is only useful to analyze a database that currently has no statistics or has wholly incorrect ones, such as if it is newly populated from a restored dump or by `pg_upgrade`. Be aware that running with this option in a database with existing statistics may cause the query optimizer choices to become transiently worse due to the low statistics targets of the early stages.
:::{/item}
:::{.item term="`-?`; `--help`"}
Show help about vacuumdb command line arguments, and exit.
:::{/item}
:::{/dl}

vacuumdb also accepts the following command-line arguments for connection parameters:

:::{.dl}
:::{.item term="`-h host`; `--host=host`"}
Specifies the host name of the machine on which the server is running. If the value begins with a slash, it is used as the directory for the Unix domain socket.
:::{/item}
:::{.item term="`-p port`; `--port=port`"}
Specifies the TCP port or local Unix domain socket file extension on which the server is listening for connections.
:::{/item}
:::{.item term="`-U username`; `--username=username`"}
User name to connect as.
:::{/item}
:::{.item term="`-w`; `--no-password`"}
Never issue a password prompt. If the server requires password authentication and a password is not available by other means such as a `.pgpass` file, the connection attempt will fail. This option can be useful in batch jobs and scripts where no user is present to enter a password.
:::{/item}
:::{.item term="`-W`; `--password`"}
Force vacuumdb to prompt for a password before connecting to a database.

This option is never essential, since vacuumdb will automatically prompt for a password if the server demands password authentication. However, vacuumdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.
:::{/item}
:::{.item term="`--maintenance-db=dbname`"}
When the `-a`/`--all` is used, connect to this database to gather the list of databases to vacuum. If not specified, the `postgres` database will be used, or if that does not exist, `template1` will be used. This can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options. Also, connection string parameters other than the database name itself will be re-used when connecting to other databases.
:::{/item}
:::{/dl}

## Environment

:::{.dl}
:::{.item term="`PGDATABASE`; `PGHOST`; `PGPORT`; `PGUSER`"}
Default connection parameters
:::{/item}
:::{.item term="`PG_COLOR`"}
Specifies whether to use color in diagnostic messages. Possible values are `always`, `auto` and `never`.
:::{/item}
:::{/dl}

This utility, like most other PostgreSQL utilities, also uses the environment variables supported by libpq (see [Environment Variables](braised:ref/libpq-envars)).

## Diagnostics

In case of difficulty, see [VACUUM](braised:ref/sql-vacuum) and [psql](braised:ref/app-psql) for discussions of potential problems and error messages.
The database server must be running at the targeted host.
Also, any default connection settings and environment variables used by the libpq front-end library will apply.

## Examples

To clean the database `test`:

    $ vacuumdb test

To clean and analyze for the optimizer a database named `bigdb`:

    $ vacuumdb --analyze bigdb

To clean a single table `foo` in a database named `xyzzy`, and analyze a single column `bar` of the table for the optimizer:

    $ vacuumdb --analyze --verbose --table='foo(bar)' xyzzy

To clean all tables in the `foo` and `bar` schemas in a database named `xyzzy`:

    $ vacuumdb --schema='foo' --schema='bar' xyzzy
