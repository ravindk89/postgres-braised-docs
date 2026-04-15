---
title: "F.49. uuid-ossp — a UUID generator"
id: uuid-ossp
---

## uuid-ossp a UUID generator

The `uuid-ossp` module provides functions to generate universally unique identifiers (UUIDs) using one of several standard algorithms.
There are also functions to produce certain special UUID constants.
This module is only necessary for special requirements beyond what is available in core PostgreSQL.
See [UUID Functions](braised:ref/functions-uuid) for built-in ways to generate UUIDs.

This module is considered "trusted", that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

### `uuid-ossp` Functions

[Functions for UUID Generation](#uuid-ossp-functions) shows the functions available to generate UUIDs.
The relevant standards ITU-T Rec.
X.667, ISO/IEC 9834-8:2005, and [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122) specify four algorithms for generating UUIDs, identified by the version numbers 1, 3, 4, and 5. (There is no version 2 algorithm.) Each of these algorithms could be suitable for a different set of applications.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_generate_v1` () uuid

   Generates a version 1 UUID. This involves the MAC address of the computer and a time stamp. Note that UUIDs of this kind reveal the identity of the computer that created the identifier and the time at which it did so, which might make it unsuitable for certain security-sensitive applications.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_generate_v1mc` () uuid

   Generates a version 1 UUID, but uses a random multicast MAC address instead of the real MAC address of the computer.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_generate_v3` ( `namespace` `uuid`, `name` `text` ) uuid

   Generates a version 3 UUID in the given namespace using the specified input name. The namespace should be one of the special constants produced by the `uuid_ns_*()` functions shown in [Functions Returning UUID Constants](#uuid-ossp-constants). (It could be any UUID in theory.) The name is an identifier in the selected namespace.

   For example:

       SELECT uuid_generate_v3(uuid_ns_url(), 'http://www.postgresql.org');

   The name parameter will be MD5-hashed, so the cleartext cannot be derived from the generated UUID. The generation of UUIDs by this method has no random or environment-dependent element and is therefore reproducible.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_generate_v4` () uuid

   Generates a version 4 UUID, which is derived entirely from random numbers.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_generate_v5` ( `namespace` `uuid`, `name` `text` ) uuid

   Generates a version 5 UUID, which works like a version 3 UUID except that SHA-1 is used as a hashing method. Version 5 should be preferred over version 3 because SHA-1 is thought to be more secure than MD5.
  :::{/cell}
  :::{/row}
:::{/table}

: Functions for UUID Generation

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_nil` () uuid

   Returns a "nil" UUID constant, which does not occur as a real UUID.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_ns_dns` () uuid

   Returns a constant designating the DNS namespace for UUIDs.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_ns_url` () uuid

   Returns a constant designating the URL namespace for UUIDs.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_ns_oid` () uuid

   Returns a constant designating the ISO object identifier (OID) namespace for UUIDs. (This pertains to ASN.1 OIDs, which are unrelated to the OIDs used in PostgreSQL.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `uuid_ns_x500` () uuid

   Returns a constant designating the X.500 distinguished name (DN) namespace for UUIDs.
  :::{/cell}
  :::{/row}
:::{/table}

: Functions Returning UUID Constants

### Building `uuid-ossp`

Historically this module depended on the OSSP UUID library, which accounts for the module\'s name. While the OSSP UUID library can still be found at [](http://www.ossp.org/pkg/lib/uuid/), it is not well maintained, and is becoming increasingly difficult to port to newer platforms. `uuid-ossp` can now be built without the OSSP library on some platforms. On FreeBSD and some other BSD-derived platforms, suitable UUID creation functions are included in the core `libc` library. On Linux, macOS, and some other platforms, suitable functions are provided in the `libuuid` library, which originally came from the `e2fsprogs` project (though on modern Linux it is considered part of `util-linux-ng`). When invoking `configure`, specify `--with-uuid=bsd` to use the BSD functions, or `--with-uuid=e2fs` to use `e2fsprogs`\' `libuuid`, or `--with-uuid=ossp` to use the OSSP UUID library. More than one of these libraries might be available on a particular machine, so `configure` does not automatically choose one.

### Author

Peter Eisentraut <peter_e@gmx.net>
