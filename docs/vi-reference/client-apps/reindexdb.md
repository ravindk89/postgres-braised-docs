---
title: "reindexdb"
layout: reference
id: app-reindexdb
description: "reindex a PostgreSQL database"
---

:::synopsis
reindexdb
 connection-option
 option

 
 
 
 -S
 --schema
 
 schema
 
 

 
 
 
 -t
 --table
 
 table
 
 

 
 
 
 -i
 --index
 
 index
 
 

 
 
 
 -s
 --system
 
 
 

 
 
 dbname
 -a
 --all
:::

## Description

reindexdb is a utility for rebuilding indexes in a PostgreSQL database.

reindexdb is a wrapper around the SQL command [`REINDEX`](#sql-reindex).
There is no effective difference between reindexing databases via this utility and via other methods for accessing the server.

## Options

reindexdb accepts the following command-line arguments:

:::{.dl}
:::{.item term="`-a`; `--all`"}
Reindex all databases.
:::{/item}
:::{.item term="`--concurrently`"}
Use the `CONCURRENTLY` option. See [REINDEX](braised:ref/sql-reindex), where all the caveats of this option are explained in detail.
:::{/item}
:::{.item term="`-d dbname`; `--dbname=dbname`"}
Specifies the name of the database to be reindexed, when `-a`/`--all` is not used. If this is not specified, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used. The *dbname* can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options.
:::{/item}
:::{.item term="`-e`; `--echo`"}
Echo the commands that reindexdb generates and sends to the server.
:::{/item}
:::{.item term="`-i index`; `--index=index`"}
Recreate *index* only. Multiple indexes can be recreated by writing multiple `-i` switches.
:::{/item}
:::{.item term="`-j njobs`; `--jobs=njobs`"}
Execute the reindex commands in parallel by running *njobs* commands simultaneously. This option may reduce the processing time but it also increases the load on the database server.

reindexdb will open *njobs* connections to the database, so make sure your [max_connections (integer)
      
   max_connections configuration parameter](braised:ref/runtime-config-connection#max-connections-integer-max-connections-configuration-parameter) setting is high enough to accommodate all connections.

Note that this option is incompatible with the `--system` option.
:::{/item}
:::{.item term="`-q`; `--quiet`"}
Do not display progress messages.
:::{/item}
:::{.item term="`-s`; `--system`"}
Reindex database\'s system catalogs only.
:::{/item}
:::{.item term="`-S schema`; `--schema=schema`"}
Reindex *schema* only. Multiple schemas can be reindexed by writing multiple `-S` switches.
:::{/item}
:::{.item term="`-t table`; `--table=table`"}
Reindex *table* only. Multiple tables can be reindexed by writing multiple `-t` switches.
:::{/item}
:::{.item term="`--tablespace=tablespace`"}
Specifies the tablespace where indexes are rebuilt. (This name is processed as a double-quoted identifier.)
:::{/item}
:::{.item term="`-v`; `--verbose`"}
Print detailed information during processing.
:::{/item}
:::{.item term="`-V`; `--version`"}
Print the reindexdb version and exit.
:::{/item}
:::{.item term="`-?`; `--help`"}
Show help about reindexdb command line arguments, and exit.
:::{/item}
:::{/dl}

reindexdb also accepts the following command-line arguments for connection parameters:

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
Force reindexdb to prompt for a password before connecting to a database.

This option is never essential, since reindexdb will automatically prompt for a password if the server demands password authentication. However, reindexdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.
:::{/item}
:::{.item term="`--maintenance-db=dbname`"}
When the `-a`/`--all` is used, connect to this database to gather the list of databases to reindex. If not specified, the `postgres` database will be used, or if that does not exist, `template1` will be used. This can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options. Also, connection string parameters other than the database name itself will be re-used when connecting to other databases.
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

In case of difficulty, see [REINDEX](braised:ref/sql-reindex) and [psql](braised:ref/app-psql) for discussions of potential problems and error messages.
The database server must be running at the targeted host.
Also, any default connection settings and environment variables used by the libpq front-end library will apply.

## Examples

To reindex the database `test`:

    $ reindexdb test

To reindex the table `foo` and the index `bar` in a database named `abcd`:

    $ reindexdb --table=foo --index=bar abcd
