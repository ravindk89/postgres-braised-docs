---
title: "32.15. Environment Variables"
id: libpq-envars
---

## Environment Variables

The following environment variables can be used to select default connection parameter values, which will be used by `PQconnectdb`, `PQsetdbLogin` and `PQsetdb` if no value is directly specified by the calling code.
These are useful to avoid hard-coding database connection information into simple client applications, for example.

-   `PGHOST` behaves the same as the [host](braised:ref/libpq-connect#host) connection parameter.

-   `PGSSLNEGOTIATION` behaves the same as the [sslnegotiation](braised:ref/libpq-connect#sslnegotiation) connection parameter.

-   `PGHOSTADDR` behaves the same as the [hostaddr](braised:ref/libpq-connect#hostaddr) connection parameter. This can be set instead of or in addition to `PGHOST` to avoid DNS lookup overhead.

-   `PGPORT` behaves the same as the [port](braised:ref/libpq-connect#port) connection parameter.

-   `PGDATABASE` behaves the same as the [dbname](braised:ref/libpq-connect#dbname) connection parameter.

-   `PGUSER` behaves the same as the [user](braised:ref/libpq-connect#user) connection parameter.

-   `PGPASSWORD` behaves the same as the [password](braised:ref/libpq-connect#password) connection parameter. Use of this environment variable is not recommended for security reasons, as some operating systems allow non-root users to see process environment variables via ps; instead consider using a password file (see [The Password File](braised:ref/libpq-pgpass)).

-   `PGPASSFILE` behaves the same as the [passfile](braised:ref/libpq-connect#passfile) connection parameter.

-   `PGREQUIREAUTH` behaves the same as the [require_auth](braised:ref/libpq-connect#require-auth) connection parameter.

-   `PGCHANNELBINDING` behaves the same as the [channel_binding](braised:ref/libpq-connect#channel-binding) connection parameter.

-   `PGSERVICE` behaves the same as the [service](braised:ref/libpq-connect#service) connection parameter.

-   `PGSERVICEFILE` specifies the name of the per-user connection service file (see [The Connection Service File](braised:ref/libpq-pgservice)). Defaults to `~/.pg_service.conf`, or `%APPDATA%\postgresql\.pg_service.conf` on Microsoft Windows.

-   `PGOPTIONS` behaves the same as the [options](braised:ref/libpq-connect#options) connection parameter.

-   `PGAPPNAME` behaves the same as the [application_name](braised:ref/libpq-connect#application-name) connection parameter.

-   `PGSSLMODE` behaves the same as the [sslmode](braised:ref/libpq-connect#sslmode) connection parameter.

-   `PGREQUIRESSL` behaves the same as the [requiressl](braised:ref/libpq-connect#requiressl) connection parameter. This environment variable is deprecated in favor of the `PGSSLMODE` variable; setting both variables suppresses the effect of this one.

-   `PGSSLCOMPRESSION` behaves the same as the [sslcompression](braised:ref/libpq-connect#sslcompression) connection parameter.

-   `PGSSLCERT` behaves the same as the [sslcert](braised:ref/libpq-connect#sslcert) connection parameter.

-   `PGSSLKEY` behaves the same as the [sslkey](braised:ref/libpq-connect#sslkey) connection parameter.

-   `PGSSLCERTMODE` behaves the same as the [sslcertmode](braised:ref/libpq-connect#sslcertmode) connection parameter.

-   `PGSSLROOTCERT` behaves the same as the [sslrootcert](braised:ref/libpq-connect#sslrootcert) connection parameter.

-   `PGSSLCRL` behaves the same as the [sslcrl](braised:ref/libpq-connect#sslcrl) connection parameter.

-   `PGSSLCRLDIR` behaves the same as the [sslcrldir](braised:ref/libpq-connect#sslcrldir) connection parameter.

-   `PGSSLSNI` behaves the same as the [sslsniServer Name Indication](braised:ref/libpq-connect#sslsniserver-name-indication) connection parameter.

-   `PGREQUIREPEER` behaves the same as the [requirepeer](braised:ref/libpq-connect#requirepeer) connection parameter.

-   `PGSSLMINPROTOCOLVERSION` behaves the same as the [ssl_min_protocol_version](braised:ref/libpq-connect#ssl-min-protocol-version) connection parameter.

-   `PGSSLMAXPROTOCOLVERSION` behaves the same as the [ssl_max_protocol_version](braised:ref/libpq-connect#ssl-max-protocol-version) connection parameter.

-   `PGGSSENCMODE` behaves the same as the [gssencmode](braised:ref/libpq-connect#gssencmode) connection parameter.

-   `PGKRBSRVNAME` behaves the same as the [krbsrvname](braised:ref/libpq-connect#krbsrvname) connection parameter.

-   `PGGSSLIB` behaves the same as the [gsslib](braised:ref/libpq-connect#gsslib) connection parameter.

-   `PGGSSDELEGATION` behaves the same as the [gssdelegation](braised:ref/libpq-connect#gssdelegation) connection parameter.

-   `PGCONNECT_TIMEOUT` behaves the same as the [connect_timeout](braised:ref/libpq-connect#connect-timeout) connection parameter.

-   `PGCLIENTENCODING` behaves the same as the [client_encoding](braised:ref/libpq-connect#client-encoding) connection parameter.

-   `PGTARGETSESSIONATTRS` behaves the same as the [target_session_attrs](braised:ref/libpq-connect#target-session-attrs) connection parameter.

-   `PGLOADBALANCEHOSTS` behaves the same as the [load_balance_hosts](braised:ref/libpq-connect#load-balance-hosts) connection parameter.

-   `PGMINPROTOCOLVERSION` behaves the same as the [min_protocol_version](braised:ref/libpq-connect#min-protocol-version) connection parameter.

-   `PGMAXPROTOCOLVERSION` behaves the same as the [max_protocol_version](braised:ref/libpq-connect#max-protocol-version) connection parameter.

The following environment variables can be used to specify default behavior for each PostgreSQL session. (See also the [ALTER ROLE](braised:ref/sql-alterrole) and [ALTER DATABASE](braised:ref/sql-alterdatabase) commands for ways to set default behavior on a per-user or per-database basis.)

-   `PGDATESTYLE` sets the default style of date/time representation. (Equivalent to `SET datestyle TO ...`.)

-   `PGTZ` sets the default time zone. (Equivalent to `SET timezone TO ...`.)

-   `PGGEQO` sets the default mode for the genetic query optimizer. (Equivalent to `SET geqo TO ...`.)

Refer to the SQL command [SET](braised:ref/sql-set) for information on correct values for these environment variables.

The following environment variables determine internal behavior of libpq; they override compiled-in defaults.

-   `PGSYSCONFDIR` sets the directory containing the `pg_service.conf` file and in a future version possibly other system-wide configuration files.

-   `PGLOCALEDIR` sets the directory containing the `locale` files for message localization.
