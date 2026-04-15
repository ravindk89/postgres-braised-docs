---
title: "45.2. Interface Support Functions"
id: spi-interface-support
---

## Interface Support Functions

The functions described here provide an interface for extracting information from result sets returned by `SPI_execute` and other SPI functions.

All functions described in this section can be used by both connected and unconnected C functions.

SPI_fname

3

SPI_fname

determine the column name for the specified column number

char \* SPI_fname(TupleDesc

rowdesc

, int

colnumber

)

## Description

`SPI_fname` returns a copy of the column name of the specified column. (You can use `pfree` to release the copy of the name when you don\'t need it anymore.)

## Arguments

:::{.dl}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`int colnumber`"}
column number (count starts at 1)
:::{/item}
:::{/dl}

## Return Value

The column name; `NULL` if `colnumber` is out of range. `SPI_result` set to `SPI_ERROR_NOATTRIBUTE` on error.

SPI_fnumber

3

SPI_fnumber

determine the column number for the specified column name

int SPI_fnumber(TupleDesc

rowdesc

, const char \*

colname

)

## Description

`SPI_fnumber` returns the column number for the column with the specified name.

If `colname` refers to a system column (e.g., `ctid`) then the appropriate negative column number will be returned.
The caller should be careful to test the return value for exact equality to `SPI_ERROR_NOATTRIBUTE` to detect an error; testing the result for less than or equal to 0 is not correct unless system columns should be rejected.

## Arguments

:::{.dl}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`const char * colname`"}
column name
:::{/item}
:::{/dl}

## Return Value

Column number (count starts at 1 for user-defined columns), or `SPI_ERROR_NOATTRIBUTE` if the named column was not found.

SPI_getvalue

3

SPI_getvalue

return the string value of the specified column

char \* SPI_getvalue(HeapTuple

row

, TupleDesc

rowdesc

, int

colnumber

)

## Description

`SPI_getvalue` returns the string representation of the value of the specified column.

The result is returned in memory allocated using `palloc`. (You can use `pfree` to release the memory when you don\'t need it anymore.)

## Arguments

:::{.dl}
:::{.item term="`HeapTuple row`"}
input row to be examined
:::{/item}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`int colnumber`"}
column number (count starts at 1)
:::{/item}
:::{/dl}

## Return Value

Column value, or `NULL` if the column is null, `colnumber` is out of range (`SPI_result` is set to `SPI_ERROR_NOATTRIBUTE`), or no output function is available (`SPI_result` is set to `SPI_ERROR_NOOUTFUNC`).

SPI_getbinval

3

SPI_getbinval

return the binary value of the specified column

Datum SPI_getbinval(HeapTuple

row

, TupleDesc

rowdesc

, int

colnumber

, bool \*

isnull

)

## Description

`SPI_getbinval` returns the value of the specified column in the internal form (as type `Datum`).

This function does not allocate new space for the datum.
In the case of a pass-by-reference data type, the return value will be a pointer into the passed row.

## Arguments

:::{.dl}
:::{.item term="`HeapTuple row`"}
input row to be examined
:::{/item}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`int colnumber`"}
column number (count starts at 1)
:::{/item}
:::{.item term="`bool * isnull`"}
flag for a null value in the column
:::{/item}
:::{/dl}

## Return Value

The binary value of the column is returned.
The variable pointed to by `isnull` is set to true if the column is null, else to false.

`SPI_result` is set to `SPI_ERROR_NOATTRIBUTE` on error.

SPI_gettype

3

SPI_gettype

return the data type name of the specified column

char \* SPI_gettype(TupleDesc

rowdesc

, int

colnumber

)

## Description

`SPI_gettype` returns a copy of the data type name of the specified column. (You can use `pfree` to release the copy of the name when you don\'t need it anymore.)

## Arguments

:::{.dl}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`int colnumber`"}
column number (count starts at 1)
:::{/item}
:::{/dl}

## Return Value

The data type name of the specified column, or `NULL` on error. `SPI_result` is set to `SPI_ERROR_NOATTRIBUTE` on error.

SPI_gettypeid

3

SPI_gettypeid

return the data type

OID

of the specified column

Oid SPI_gettypeid(TupleDesc

rowdesc

, int

colnumber

)

## Description

`SPI_gettypeid` returns the OID of the data type of the specified column.

## Arguments

:::{.dl}
:::{.item term="`TupleDesc rowdesc`"}
input row description
:::{/item}
:::{.item term="`int colnumber`"}
column number (count starts at 1)
:::{/item}
:::{/dl}

## Return Value

The OID of the data type of the specified column or `InvalidOid` on error.
On error, `SPI_result` is set to `SPI_ERROR_NOATTRIBUTE`.

SPI_getrelname

3

SPI_getrelname

return the name of the specified relation

char \* SPI_getrelname(Relation

rel

)

## Description

`SPI_getrelname` returns a copy of the name of the specified relation. (You can use `pfree` to release the copy of the name when you don\'t need it anymore.)

## Arguments

:::{.dl}
:::{.item term="`Relation rel`"}
input relation
:::{/item}
:::{/dl}

## Return Value

The name of the specified relation.

SPI_getnspname

3

SPI_getnspname

return the namespace of the specified relation

char \* SPI_getnspname(Relation

rel

)

## Description

`SPI_getnspname` returns a copy of the name of the namespace that the specified Relation belongs to.
This is equivalent to the relation\'s schema.
You should `pfree` the return value of this function when you are finished with it.

## Arguments

:::{.dl}
:::{.item term="`Relation rel`"}
input relation
:::{/item}
:::{/dl}

## Return Value

The name of the specified relation\'s namespace.

SPI_result_code_string

3

SPI_result_code_string

return error code as string

const char \* SPI_result_code_string(int

code

);

## Description

`SPI_result_code_string` returns a string representation of the result code returned by various SPI functions or stored in `SPI_result`.

## Arguments

:::{.dl}
:::{.item term="`int code`"}
result code
:::{/item}
:::{/dl}

## Return Value

A string representation of the result code.
