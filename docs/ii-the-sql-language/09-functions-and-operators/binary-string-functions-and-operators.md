---
title: "9.5. Binary String Functions and Operators"
id: functions-binarystring
---

## Binary String Functions and Operators

This section describes functions and operators for examining and manipulating binary strings, that is values of type `bytea`.
Many of these are equivalent, in purpose and syntax, to the text-string functions described in the previous section.

SQL defines some string functions that use key words, rather than commas, to separate arguments.
Details are in [Binary String Functions and Operators](#functions-binarystring-sql).
PostgreSQL also provides versions of these functions that use the regular function invocation syntax (see [Other Binary String Functions](#functions-binarystring-other)).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function/Operator

   Description

   Example(s)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bytea` `||` `bytea` bytea

   Concatenates the two binary strings.

   `'\x123456'::bytea || '\x789a00bcde'::bytea` \\x123456789a00bcde
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bit_length` ( `bytea` ) integer

   Returns number of bits in the binary string (8 times the `octet_length`).

   `bit_length('\x123456'::bytea)` 24
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `btrim` ( `bytes` `bytea`, `bytesremoved` `bytea` ) bytea

   Removes the longest string containing only bytes appearing in `bytesremoved` from the start and end of `bytes`.

   `btrim('\x1234567890'::bytea, '\x9012'::bytea)` \\x345678
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `ltrim` ( `bytes` `bytea`, `bytesremoved` `bytea` ) bytea

   Removes the longest string containing only bytes appearing in `bytesremoved` from the start of `bytes`.

   `ltrim('\x1234567890'::bytea, '\x9012'::bytea)` \\x34567890
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `octet_length` ( `bytea` ) integer

   Returns number of bytes in the binary string.

   `octet_length('\x123456'::bytea)` 3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `overlay` ( `bytes` `bytea` `PLACING` `newsubstring` `bytea` `FROM` `start` `integer` \[`FOR` `count` `integer`\] ) bytea

   Replaces the substring of `bytes` that starts at the `start`\'th byte and extends for `count` bytes with `newsubstring`. If `count` is omitted, it defaults to the length of `newsubstring`.

   `overlay('\x1234567890'::bytea placing '\002\003'::bytea from 2 for 3)` \\x12020390
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `position` ( `substring` `bytea` `IN` `bytes` `bytea` ) integer

   Returns first starting index of the specified `substring` within `bytes`, or zero if it\'s not present.

   `position('\x5678'::bytea in '\x1234567890'::bytea)` 3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `rtrim` ( `bytes` `bytea`, `bytesremoved` `bytea` ) bytea

   Removes the longest string containing only bytes appearing in `bytesremoved` from the end of `bytes`.

   `rtrim('\x1234567890'::bytea, '\x9012'::bytea)` \\x12345678
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `substring` ( `bytes` `bytea` \[`FROM` `start` `integer`\] \[`FOR` `count` `integer`\] ) bytea

   Extracts the substring of `bytes` starting at the `start`\'th byte if that is specified, and stopping after `count` bytes if that is specified. Provide at least one of `start` and `count`.

   `substring('\x1234567890'::bytea from 3 for 2)` \\x5678
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `trim` ( \[`LEADING` \| `TRAILING` \| `BOTH`\] `bytesremoved` `bytea` `FROM` `bytes` `bytea` ) bytea

   Removes the longest string containing only bytes appearing in `bytesremoved` from the start, end, or both ends (`BOTH` is the default) of `bytes`.

   `trim('\x9012'::bytea from '\x1234567890'::bytea)` \\x345678
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `trim` ( \[`LEADING` \| `TRAILING` \| `BOTH`\] \[`FROM`\] `bytes` `bytea`, `bytesremoved` `bytea` ) bytea

   This is a non-standard syntax for `trim()`.

   `trim(both from '\x1234567890'::bytea, '\x9012'::bytea)` \\x345678
  :::{/cell}
  :::{/row}
:::{/table}

: SQL Binary String Functions and Operators

Additional binary string manipulation functions are available and are listed in [Other Binary String Functions](#functions-binarystring-other). Some of them are used internally to implement the SQL-standard string functions listed in [Binary String Functions and Operators](#functions-binarystring-sql).

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
   `bit_count` ( `bytes` `bytea` ) bigint

   Returns the number of bits set in the binary string (also known as "popcount").

   `bit_count('\x1234567890'::bytea)` 15
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `crc32` ( `bytea` ) bigint

   Computes the CRC-32 value of the binary string.

   `crc32('abc'::bytea)` 891568578
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `crc32c` ( `bytea` ) bigint

   Computes the CRC-32C value of the binary string.

   `crc32c('abc'::bytea)` 910901175
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `get_bit` ( `bytes` `bytea`, `n` `bigint` ) integer

   Extracts [n\'th](#functions-zerobased-note) bit from binary string.

   `get_bit('\x1234567890'::bytea, 30)` 1
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `get_byte` ( `bytes` `bytea`, `n` `integer` ) integer

   Extracts [n\'th](#functions-zerobased-note) byte from binary string.

   `get_byte('\x1234567890'::bytea, 4)` 144
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `length` ( `bytea` ) integer

   Returns the number of bytes in the binary string.

   `length('\x1234567890'::bytea)` 5
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `length` ( `bytes` `bytea`, `encoding` `name` ) integer

   Returns the number of characters in the binary string, assuming that it is text in the given `encoding`.

   `length('jose'::bytea, 'UTF8')` 4
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `md5` ( `bytea` ) text

   Computes the MD5 [hash](#functions-hash-note) of the binary string, with the result written in hexadecimal.

   `md5('Th\000omas'::bytea)` 8ab2d3c9689aaf18​b4958c334c82d8b1
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `reverse` ( `bytea` ) bytea

   Reverses the order of the bytes in the binary string.

   `reverse('\xabcd'::bytea)` \\xcdab
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `set_bit` ( `bytes` `bytea`, `n` `bigint`, `newvalue` `integer` ) bytea

   Sets [n\'th](#functions-zerobased-note) bit in binary string to `newvalue`.

   `set_bit('\x1234567890'::bytea, 30, 0)` \\x1234563890
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `set_byte` ( `bytes` `bytea`, `n` `integer`, `newvalue` `integer` ) bytea

   Sets [n\'th](#functions-zerobased-note) byte in binary string to `newvalue`.

   `set_byte('\x1234567890'::bytea, 4, 64)` \\x1234567840
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sha224` ( `bytea` ) bytea

   Computes the SHA-224 [hash](#functions-hash-note) of the binary string.

   `sha224('abc'::bytea)` \\x23097d223405d8228642a477bda2​55b32aadbce4bda0b3f7e36c9da7
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sha256` ( `bytea` ) bytea

   Computes the SHA-256 [hash](#functions-hash-note) of the binary string.

   `sha256('abc'::bytea)` \\xba7816bf8f01cfea414140de5dae2223​b00361a396177a9cb410ff61f20015ad
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sha384` ( `bytea` ) bytea

   Computes the SHA-384 [hash](#functions-hash-note) of the binary string.

   `sha384('abc'::bytea)` \\xcb00753f45a35e8bb5a03d699ac65007​272c32ab0eded1631a8b605a43ff5bed​8086072ba1e7cc2358baeca134c825a7
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sha512` ( `bytea` ) bytea

   Computes the SHA-512 [hash](#functions-hash-note) of the binary string.

   `sha512('abc'::bytea)` \\xddaf35a193617abacc417349ae204131​12e6fa4e89a97ea20a9eeee64b55d39a​2192992a274fc1a836ba3c23a3feebbd​454d4423643ce80e2a9ac94fa54ca49f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `substr` ( `bytes` `bytea`, `start` `integer` \[, `count` `integer`\] ) bytea

   Extracts the substring of `bytes` starting at the `start`\'th byte, and extending for `count` bytes if that is specified. (Same as `substring(bytes from start for count)`.)

   `substr('\x1234567890'::bytea, 3, 2)` \\x5678
  :::{/cell}
  :::{/row}
:::{/table}

: Other Binary String Functions

Functions `get_byte` and `set_byte` number the first byte of a binary string as byte 0. Functions `get_bit` and `set_bit` number bits from the right within each byte; for example bit 0 is the least significant bit of the first byte, and bit 15 is the most significant bit of the second byte.

For historical reasons, the function `md5` returns a hex-encoded value of type `text` whereas the SHA-2 functions return type `bytea`. Use the functions [`encode`](#function-encode) and [`decode`](#function-decode) to convert between the two. For example write `encode(sha256('abc'), 'hex')` to get a hex-encoded text representation, or `decode(md5('abc'), 'hex')` to get a `bytea` value.

[Text/Binary String Conversion Functions](#functions-binarystring-conversions). For these functions, an argument or result of type `text` is expressed in the database\'s default encoding, while arguments or results of type `bytea` are in an encoding named by another argument.

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
   `convert` ( `bytes` `bytea`, `src_encoding` `name`, `dest_encoding` `name` ) bytea

   Converts a binary string representing text in encoding `src_encoding` to a binary string in encoding `dest_encoding` (see [Available Character Set Conversions](braised:ref/multibyte#available-character-set-conversions) for available conversions).

   `convert('text_in_utf8', 'UTF8', 'LATIN1')` \\x746578745f696e5f75746638
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `convert_from` ( `bytes` `bytea`, `src_encoding` `name` ) text

   Converts a binary string representing text in encoding `src_encoding` to `text` in the database encoding (see [Available Character Set Conversions](braised:ref/multibyte#available-character-set-conversions) for available conversions).

   `convert_from('text_in_utf8', 'UTF8')` text_in_utf8
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `convert_to` ( `string` `text`, `dest_encoding` `name` ) bytea

   Converts a `text` string (in the database encoding) to a binary string encoded in encoding `dest_encoding` (see [Available Character Set Conversions](braised:ref/multibyte#available-character-set-conversions) for available conversions).

   `convert_to('some_text', 'UTF8')` \\x736f6d655f74657874
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `encode` ( `bytes` `bytea`, `format` `text` ) text

   Encodes binary data into a textual representation; supported `format` values are: [`base64`](#encode-format-base64), [`escape`](#encode-format-escape), [`hex`](#encode-format-hex).

   `encode('123\000\001', 'base64')` MTIzAAE=
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `decode` ( `string` `text`, `format` `text` ) bytea

   Decodes binary data from a textual representation; supported `format` values are the same as for `encode`.

   `decode('MTIzAAE=', 'base64')` \\x3132330001
  :::{/cell}
  :::{/row}
:::{/table}

: Text/Binary String Conversion Functions

The `encode` and `decode` functions support the following textual formats:

:::{.dl}
:::{.item term="base64"}
The `base64` format is that of [RFC 2045 Section 6.8](https://datatracker.ietf.org/doc/html/rfc2045#section-6.8). As per the RFC, encoded lines are broken at 76 characters. However instead of the MIME CRLF end-of-line marker, only a newline is used for end-of-line. The `decode` function ignores carriage-return, newline, space, and tab characters. Otherwise, an error is raised when `decode` is supplied invalid base64 data including when trailing padding is incorrect.
:::{/item}
:::{.item term="escape"}
The `escape` format converts zero bytes and bytes with the high bit set into octal escape sequences (`\`*nnn*), and it doubles backslashes. Other byte values are represented literally. The `decode` function will raise an error if a backslash is not followed by either a second backslash or three octal digits; it accepts other byte values unchanged.
:::{/item}
:::{.item term="hex"}
The `hex` format represents each 4 bits of data as one hexadecimal digit, `0` through `f`, writing the higher-order digit of each byte first. The `encode` function outputs the `a`-`f` hex digits in lower case. Because the smallest unit of data is 8 bits, there are always an even number of characters returned by `encode`. The `decode` function accepts the `a`-`f` characters in either upper or lower case. An error is raised when `decode` is given invalid hex data including when given an odd number of characters.
:::{/item}
:::{/dl}

In addition, it is possible to cast integral values to and from type `bytea`. Casting an integer to `bytea` produces 2, 4, or 8 bytes, depending on the width of the integer type. The result is the two\'s complement representation of the integer, with the most significant byte first. Some examples:

    1234::smallint::bytea          \x04d2
    cast(1234 as bytea)            \x000004d2
    cast(-1234 as bytea)           \xfffffb2e
    '\x8000'::bytea::smallint      -32768
    '\x8000'::bytea::integer       32768

Casting a `bytea` to an integer will raise an error if the length of the `bytea` exceeds the width of the integer type.

See also the aggregate function `string_agg` in [Aggregate Functions](braised:ref/functions-aggregate) and the large object functions in [Server-Side Functions](braised:ref/lo-funcs).
