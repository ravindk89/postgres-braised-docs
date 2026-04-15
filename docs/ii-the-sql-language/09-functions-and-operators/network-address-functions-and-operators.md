---
title: "9.12. Network Address Functions and Operators"
id: functions-net
---

## Network Address Functions and Operators

The IP network address types, `cidr` and `inet`, support the usual comparison operators shown in [Comparison Operators](braised:ref/functions-comparison#comparison-operators) as well as the specialized operators and functions shown in IP Address Operators and IP Address Functions.

Any `cidr` value can be cast to `inet` implicitly; therefore, the operators and functions shown below as operating on `inet` also work on `cidr` values. (Where there are separate functions for `inet` and `cidr`, it is because the behavior should be different for the two cases.) Also, it is permitted to cast an `inet` value to `cidr`.
When this is done, any bits to the right of the netmask are silently zeroed to create a valid `cidr` value.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Operator

   Description

   Example(s)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `<<` `inet` boolean

   Is subnet strictly contained by subnet? This operator, and the next four, test for subnet inclusion. They consider only the network parts of the two addresses (ignoring any bits to the right of the netmasks) and determine whether one network is identical to or a subnet of the other.

   `inet '192.168.1.5' << inet '192.168.1/24'` t

   `inet '192.168.0.5' << inet '192.168.1/24'` f

   `inet '192.168.1/24' << inet '192.168.1/24'` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `<<=` `inet` boolean

   Is subnet contained by or equal to subnet?

   `inet '192.168.1/24' <<= inet '192.168.1/24'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `>>` `inet` boolean

   Does subnet strictly contain subnet?

   `inet '192.168.1/24' >> inet '192.168.1.5'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `>>=` `inet` boolean

   Does subnet contain or equal subnet?

   `inet '192.168.1/24' >>= inet '192.168.1/24'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `&&` `inet` boolean

   Does either subnet contain or equal the other?

   `inet '192.168.1/24' && inet '192.168.1.80/28'` t

   `inet '192.168.1/24' && inet '192.168.2.0/28'` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `~` `inet` inet

   Computes bitwise NOT.

   `~ inet '192.168.1.6'` 63.87.254.249
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `&` `inet` inet

   Computes bitwise AND.

   `inet '192.168.1.6' & inet '0.0.0.255'` 0.0.0.6
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `|` `inet` inet

   Computes bitwise OR.

   `inet '192.168.1.6' | inet '0.0.0.255'` 192.168.1.255
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `+` `bigint` inet

   Adds an offset to an address.

   `inet '192.168.1.6' + 25` 192.168.1.31
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bigint` `+` `inet` inet

   Adds an offset to an address.

   `200 + inet '::ffff:fff0:1'` ::ffff:255.240.0.201
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `-` `bigint` inet

   Subtracts an offset from an address.

   `inet '192.168.1.43' - 36` 192.168.1.7
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet` `-` `inet` bigint

   Computes the difference of two addresses.

   `inet '192.168.1.43' - inet '192.168.1.19'` 24

   `inet '::1' - inet '::ffff:1'` -4294901760
  :::{/cell}
  :::{/row}
:::{/table}

: IP Address Operators

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description

   Example(s)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `abbrev` ( `inet` ) text

   Creates an abbreviated display format as text. (The result is the same as the `inet` output function produces; it is "abbreviated" only in comparison to the result of an explicit cast to `text`, which for historical reasons will never suppress the netmask part.)

   `abbrev(inet '10.1.0.0/32')` 10.1.0.0
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `abbrev` ( `cidr` ) text

   Creates an abbreviated display format as text. (The abbreviation consists of dropping all-zero octets to the right of the netmask; more examples are in [cidr Type Input Examples](braised:ref/datatype-net-types#cidr-type-input-examples).)

   `abbrev(cidr '10.1.0.0/16')` 10.1/16
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `broadcast` ( `inet` ) inet

   Computes the broadcast address for the address\'s network.

   `broadcast(inet '192.168.1.5/24')` 192.168.1.255/24
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `family` ( `inet` ) integer

   Returns the address\'s family: `4` for IPv4, `6` for IPv6.

   `family(inet '::1')` 6
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `host` ( `inet` ) text

   Returns the IP address as text, ignoring the netmask.

   `host(inet '192.168.1.0/24')` 192.168.1.0
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `hostmask` ( `inet` ) inet

   Computes the host mask for the address\'s network.

   `hostmask(inet '192.168.23.20/30')` 0.0.0.3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet_merge` ( `inet`, `inet` ) cidr

   Computes the smallest network that includes both of the given networks.

   `inet_merge(inet '192.168.1.5/24', inet '192.168.2.5/24')` 192.168.0.0/22
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `inet_same_family` ( `inet`, `inet` ) boolean

   Tests whether the addresses belong to the same IP family.

   `inet_same_family(inet '192.168.1.5/24', inet '::1')` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `masklen` ( `inet` ) integer

   Returns the netmask length in bits.

   `masklen(inet '192.168.1.5/24')` 24
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `netmask` ( `inet` ) inet

   Computes the network mask for the address\'s network.

   `netmask(inet '192.168.1.5/24')` 255.255.255.0
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `network` ( `inet` ) cidr

   Returns the network part of the address, zeroing out whatever is to the right of the netmask. (This is equivalent to casting the value to `cidr`.)

   `network(inet '192.168.1.5/24')` 192.168.1.0/24
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `set_masklen` ( `inet`, `integer` ) inet

   Sets the netmask length for an `inet` value. The address part does not change.

   `set_masklen(inet '192.168.1.5/24', 16)` 192.168.1.5/16
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `set_masklen` ( `cidr`, `integer` ) cidr

   Sets the netmask length for a `cidr` value. Address bits to the right of the new netmask are set to zero.

   `set_masklen(cidr '192.168.1.0/24', 16)` 192.168.0.0/16
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `text` ( `inet` ) text

   Returns the unabbreviated IP address and netmask length as text. (This has the same result as an explicit cast to `text`.)

   `text(inet '192.168.1.5')` 192.168.1.5/32
  :::{/cell}
  :::{/row}
:::{/table}

: IP Address Functions

:::{.callout type="tip"}
The `abbrev`, `host`, and `text` functions are primarily intended to offer alternative display formats for IP addresses.
:::

The MAC address types, `macaddr` and `macaddr8`, support the usual comparison operators shown in [Comparison Operators](braised:ref/functions-comparison#comparison-operators) as well as the specialized functions shown in MAC Address Functions.
In addition, they support the bitwise logical operators `~`, `&` and `|` (NOT, AND and OR), just as shown above for IP addresses.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description

   Example(s)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `trunc` ( `macaddr` ) macaddr

   Sets the last 3 bytes of the address to zero. The remaining prefix can be associated with a particular manufacturer (using data not included in PostgreSQL).

   `trunc(macaddr '12:34:56:78:90:ab')` 12:34:56:00:00:00
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `trunc` ( `macaddr8` ) macaddr8

   Sets the last 5 bytes of the address to zero. The remaining prefix can be associated with a particular manufacturer (using data not included in PostgreSQL).

   `trunc(macaddr8 '12:34:56:78:90:ab:cd:ef')` 12:34:56:00:00:00:00:00
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `macaddr8_set7bit` ( `macaddr8` ) macaddr8

   Sets the 7th bit of the address to one, creating what is known as modified EUI-64, for inclusion in an IPv6 address.

   `macaddr8_set7bit(macaddr8 '00:34:56:ab:cd:ef')` 02:34:56:ff:fe:ab:cd:ef
  :::{/cell}
  :::{/row}
:::{/table}

: MAC Address Functions
