---
title: "clusterdb"
layout: reference
id: app-clusterdb
description: "cluster a PostgreSQL database"
---

:::synopsis
clusterdb
 connection-option
 option

 
 
 
 --table
 -t
 
 table
 
 

 
 
 dbname
 -a
 --all
:::

## Description

clusterdb is a utility for reclustering tables in a PostgreSQL database.
It finds tables that have previously been clustered, and clusters them again on the same index that was last used.
Tables that have never been clustered are not affected.

clusterdb is a wrapper around the SQL command [CLUSTER](braised:ref/sql-cluster).
There is no effective difference between clustering databases via this utility and via other methods for accessing the server.

## Options

clusterdb accepts the following command-line arguments:

:::{.dl}
:::{.item term="`-a`; `--all`"}
Cluster all databases.
:::{/item}
:::{.item term="`-d dbname`; `--dbname=dbname`"}
Specifies the name of the database to be clustered, when `-a`/`--all` is not used. If this is not specified, the database name is read from the environment variable `PGDATABASE`. If that is not set, the user name specified for the connection is used. The *dbname* can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options.
:::{/item}
:::{.item term="`-e`; `--echo`"}
Echo the commands that clusterdb generates and sends to the server.
:::{/item}
:::{.item term="`-q`; `--quiet`"}
Do not display progress messages.
:::{/item}
:::{.item term="`-t table`; `--table=table`"}
Cluster *table* only. Multiple tables can be clustered by writing multiple `-t` switches.
:::{/item}
:::{.item term="`-v`; `--verbose`"}
Print detailed information during processing.
:::{/item}
:::{.item term="`-V`; `--version`"}
Print the clusterdb version and exit.
:::{/item}
:::{.item term="`-?`; `--help`"}
Show help about clusterdb command line arguments, and exit.
:::{/item}
:::{/dl}

clusterdb also accepts the following command-line arguments for connection parameters:

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
Force clusterdb to prompt for a password before connecting to a database.

This option is never essential, since clusterdb will automatically prompt for a password if the server demands password authentication. However, clusterdb will waste a connection attempt finding out that the server wants a password. In some cases it is worth typing `-W` to avoid the extra connection attempt.
:::{/item}
:::{.item term="`--maintenance-db=dbname`"}
When the `-a`/`--all` is used, connect to this database to gather the list of databases to cluster. If not specified, the `postgres` database will be used, or if that does not exist, `template1` will be used. This can be a [connection string](#libpq-connstring). If so, connection string parameters will override any conflicting command line options. Also, connection string parameters other than the database name itself will be re-used when connecting to other databases.
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

In case of difficulty, see [CLUSTER](braised:ref/sql-cluster) and [psql](braised:ref/app-psql) for discussions of potential problems and error messages.
The database server must be running at the targeted host.
Also, any default connection settings and environment variables used by the libpq front-end library will apply.

## Examples

To cluster the database `test`:

    $ clusterdb test

To cluster a single table `foo` in a database named `xyzzy`:

    $ clusterdb --table=foo xyzzy
