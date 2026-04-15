---
title: "8.4. Binary Data Types"
id: datatype-binary
---

## Binary Data Types

The `bytea` data type allows storage of binary strings; see Binary Data Types.

----------------------------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Storage Size
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bytea`
  :::{/cell}
  :::{.cell}
  1 or 4 bytes plus the actual binary string
  :::{/cell}
  :::{.cell}
  variable-length binary string
  :::{/cell}
  :::{/row}
:::{/table}

  ----------------------------------------------------------------------------------------

  : Binary Data Types

A binary string is a sequence of octets (or bytes). Binary strings are distinguished from character strings in two ways. First, binary strings specifically allow storing octets of value zero and other "non-printable" octets (usually, octets outside the decimal range 32 to 126). Character strings disallow zero octets, and also disallow any other octet values and sequences of octet values that are invalid according to the database\'s selected character set encoding. Second, operations on binary strings process the actual bytes, whereas the processing of character strings depends on locale settings. In short, binary strings are appropriate for storing data that the programmer thinks of as "raw bytes", whereas character strings are appropriate for storing text.

The `bytea` type supports two formats for input and output: "hex" format and PostgreSQL\'s historical "escape" format. Both of these are always accepted on input. The output format depends on the configuration parameter [bytea_output (enum)
      
       bytea_output configuration parameter](braised:ref/runtime-config-client#bytea-output-enum-bytea-output-configuration-parameter); the default is hex. (Note that the hex format was introduced in PostgreSQL 9.0; earlier versions and some tools don\'t understand it.)

The SQL standard defines a different binary string type, called `BLOB` or `BINARY LARGE OBJECT`. The input format is different from `bytea`, but the provided functions and operators are mostly the same.

### `bytea` Hex Format

The "hex" format encodes binary data as 2 hexadecimal digits per byte, most significant nibble first. The entire string is preceded by the sequence `\x` (to distinguish it from the escape format). In some contexts, the initial backslash may need to be escaped by doubling it (see [String Constants](braised:ref/sql-syntax-lexical#string-constants)). For input, the hexadecimal digits can be either upper or lower case, and whitespace is permitted between digit pairs (but not within a digit pair nor in the starting `\x` sequence). The hex format is compatible with a wide range of external applications and protocols, and it tends to be faster to convert than the escape format, so its use is preferred.

Example:

    SET bytea_output = 'hex';

    SELECT '\xDEADBEEF'::bytea;
       bytea
    ------------
     \xdeadbeef

### `bytea` Escape Format

The "escape" format is the traditional PostgreSQL format for the `bytea` type. It takes the approach of representing a binary string as a sequence of ASCII characters, while converting those bytes that cannot be represented as an ASCII character into special escape sequences. If, from the point of view of the application, representing bytes as characters makes sense, then this representation can be convenient. But in practice it is usually confusing because it fuzzes up the distinction between binary strings and character strings, and also the particular escape mechanism that was chosen is somewhat unwieldy. Therefore, this format should probably be avoided for most new applications.

When entering `bytea` values in escape format, octets of certain values *must* be escaped, while all octet values *can* be escaped. In general, to escape an octet, convert it into its three-digit octal value and precede it by a backslash. Backslash itself (octet decimal value 92) can alternatively be represented by double backslashes. [Literal Escaped Octets](#datatype-binary-sqlesc) shows the characters that must be escaped, and gives the alternative escape sequences where applicable.

  -----------------------------------------------------------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Decimal Octet Value
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{.cell}
  Escaped Input Representation
  :::{/cell}
  :::{.cell}
  Example
  :::{/cell}
  :::{.cell}
  Hex Representation
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  0
  :::{/cell}
  :::{.cell}
  zero octet
  :::{/cell}
  :::{.cell}
  `'\000'`
  :::{/cell}
  :::{.cell}
  `'\000'::bytea`
  :::{/cell}
  :::{.cell}
  `\x00`
  :::{/cell}
  :::{/row}
:::{/table}

  39                       single quote             `''''` or `'\047'`             `''''::bytea`     `\x27`

  92                       backslash                `'\\'` or `'\134'`             `'\\'::bytea`     `\x5c`

  0 to 31 and 127 to 255   "non-printable" octets   `'\xxx'` (octal value)         `'\001'::bytea`   `\x01`
  -----------------------------------------------------------------------------------------------------------------------

  : `bytea` Literal Escaped Octets

The requirement to escape *non-printable* octets varies depending on locale settings. In some instances you can get away with leaving them unescaped.

The reason that single quotes must be doubled, as shown in [Literal Escaped Octets](#datatype-binary-sqlesc), is that this is true for any string literal in an SQL command. The generic string-literal parser consumes the outermost single quotes and reduces any pair of single quotes to one data character. What the `bytea` input function sees is just one single quote, which it treats as a plain data character. However, the `bytea` input function treats backslashes as special, and the other behaviors shown in [Literal Escaped Octets](#datatype-binary-sqlesc) are implemented by that function.

In some contexts, backslashes must be doubled compared to what is shown above, because the generic string-literal parser will also reduce pairs of backslashes to one data character; see [String Constants](braised:ref/sql-syntax-lexical#string-constants).

`Bytea` octets are output in `hex` format by default. If you change [bytea_output (enum)
      
       bytea_output configuration parameter](braised:ref/runtime-config-client#bytea-output-enum-bytea-output-configuration-parameter) to `escape`, "non-printable" octets are converted to their equivalent three-digit octal value and preceded by one backslash. Most "printable" octets are output by their standard representation in the client character set, e.g.:

    SET bytea_output = 'escape';

    SELECT 'abc \153\154\155 \052\251\124'::bytea;
         bytea
    ----------------
     abc klm *\251T

The octet with decimal value 92 (backslash) is doubled in the output. Details are in [Output Escaped Octets](#datatype-binary-resesc).

  -------------------------------------------------------------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Decimal Octet Value
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{.cell}
  Escaped Output Representation
  :::{/cell}
  :::{.cell}
  Example
  :::{/cell}
  :::{.cell}
  Output Result
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  92
  :::{/cell}
  :::{.cell}
  backslash
  :::{/cell}
  :::{.cell}
  `\\`
  :::{/cell}
  :::{.cell}
  `'\134'::bytea`
  :::{/cell}
  :::{.cell}
  `\\`
  :::{/cell}
  :::{/row}
:::{/table}

  0 to 31 and 127 to 255   "non-printable" octets   `\xxx` (octal value)                  `'\001'::bytea`   `\001`

  32 to 126                "printable" octets       client character set representation   `'\176'::bytea`   `~`
  -------------------------------------------------------------------------------------------------------------------------

  : `bytea` Output Escaped Octets

Depending on the front end to PostgreSQL you use, you might have additional work to do in terms of escaping and unescaping `bytea` strings. For example, you might also have to escape line feeds and carriage returns if your interface automatically translates these.
