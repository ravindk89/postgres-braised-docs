---
title: "20.12. Certificate Authentication"
id: auth-cert
---

## Certificate Authentication

This authentication method uses SSL client certificates to perform authentication.
It is therefore only available for SSL connections; see [OpenSSL Configuration](braised:ref/ssl-tcp#openssl-configuration) for SSL configuration instructions.
When using this authentication method, the server will require that the client provide a valid, trusted certificate.
No password prompt will be sent to the client.
The `cn` (Common Name) attribute of the certificate will be compared to the requested database user name, and if they match the login will be allowed.
User name mapping can be used to allow `cn` to be different from the database user name.

The following configuration options are supported for SSL certificate authentication:

:::{.dl}
:::{.item term="`map`"}
Allows for mapping between system and database user names. See [User Name Maps](braised:ref/auth-username-maps) for details.
:::{/item}
:::{/dl}

It is redundant to use the `clientcert` option with `cert` authentication because `cert` authentication is effectively `trust` authentication with `clientcert=verify-full`.
