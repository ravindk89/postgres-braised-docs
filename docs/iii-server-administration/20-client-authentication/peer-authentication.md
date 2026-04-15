---
title: "20.9. Peer Authentication"
id: auth-peer
---

## Peer Authentication

The peer authentication method works by obtaining the client\'s operating system user name from the kernel and using it as the allowed database user name (with optional user name mapping).
This method is only supported on local connections.

The following configuration options are supported for `peer`:

:::{.dl}
:::{.item term="`map`"}
Allows for mapping between system and database user names. See [User Name Maps](braised:ref/auth-username-maps) for details.
:::{/item}
:::{/dl}

Peer authentication is only available on operating systems providing the `getpeereid()` function, the `SO_PEERCRED` socket parameter, or similar mechanisms.
Currently that includes `Linux`, most flavors of `BSD` including `macOS`, and `Solaris`.
