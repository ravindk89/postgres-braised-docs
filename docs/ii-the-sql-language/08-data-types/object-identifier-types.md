---
title: "8.19. Object Identifier Types"
id: datatype-oid
---

## Object Identifier Types

Object identifiers (OIDs) are used internally by PostgreSQL as primary keys for various system tables.
Type `oid` represents an object identifier.
There are also several alias types for `oid`, each named `regsomething`. Object Identifier Types shows an overview.

The `oid` type is currently implemented as an unsigned four-byte integer.
Therefore, it is not large enough to provide database-wide uniqueness in large databases, or even in large individual tables.

The `oid` type itself has few operations beyond comparison.
It can be cast to integer, however, and then manipulated using the standard integer operators. (Beware of possible signed-versus-unsigned confusion if you do this.)

The OID alias types have no operations of their own except for specialized input and output routines.
These routines are able to accept and display symbolic names for system objects, rather than the raw numeric value that type `oid` would use.
The alias types allow simplified lookup of OID values for objects.
For example, to examine the pg_attribute rows related to a table `mytable`, one could write:

    SELECT * FROM pg_attribute WHERE attrelid = 'mytable'::regclass;

rather than:

    SELECT * FROM pg_attribute
      WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = 'mytable');

While that doesn\'t look all that bad by itself, it\'s still oversimplified.
A far more complicated sub-select would be needed to select the right OID if there are multiple tables named `mytable` in different schemas.
The `regclass` input converter handles the table lookup according to the schema path setting, and so it does the "right thing" automatically.
Similarly, casting a table\'s OID to `regclass` is handy for symbolic display of a numeric OID.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  References
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{.cell}
  Value Example
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `oid`
  :::{/cell}
  :::{.cell}
  any
  :::{/cell}
  :::{.cell}
  numeric object identifier
  :::{/cell}
  :::{.cell}
  `564182`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regclass`
  :::{/cell}
  :::{.cell}
  pg_class
  :::{/cell}
  :::{.cell}
  relation name
  :::{/cell}
  :::{.cell}
  `pg_type`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regcollation`
  :::{/cell}
  :::{.cell}
  pg_collation
  :::{/cell}
  :::{.cell}
  collation name
  :::{/cell}
  :::{.cell}
  `"POSIX"`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regconfig`
  :::{/cell}
  :::{.cell}
  pg_ts_config
  :::{/cell}
  :::{.cell}
  text search configuration
  :::{/cell}
  :::{.cell}
  `english`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regdictionary`
  :::{/cell}
  :::{.cell}
  pg_ts_dict
  :::{/cell}
  :::{.cell}
  text search dictionary
  :::{/cell}
  :::{.cell}
  `simple`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regnamespace`
  :::{/cell}
  :::{.cell}
  pg_namespace
  :::{/cell}
  :::{.cell}
  namespace name
  :::{/cell}
  :::{.cell}
  `pg_catalog`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regoper`
  :::{/cell}
  :::{.cell}
  pg_operator
  :::{/cell}
  :::{.cell}
  operator name
  :::{/cell}
  :::{.cell}
  `+`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regoperator`
  :::{/cell}
  :::{.cell}
  pg_operator
  :::{/cell}
  :::{.cell}
  operator with argument types
  :::{/cell}
  :::{.cell}
  `*(integer,​integer)` or `-(NONE,​integer)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regproc`
  :::{/cell}
  :::{.cell}
  pg_proc
  :::{/cell}
  :::{.cell}
  function name
  :::{/cell}
  :::{.cell}
  `sum`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regprocedure`
  :::{/cell}
  :::{.cell}
  pg_proc
  :::{/cell}
  :::{.cell}
  function with argument types
  :::{/cell}
  :::{.cell}
  `sum(int4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regrole`
  :::{/cell}
  :::{.cell}
  pg_authid
  :::{/cell}
  :::{.cell}
  role name
  :::{/cell}
  :::{.cell}
  `smithee`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `regtype`
  :::{/cell}
  :::{.cell}
  pg_type
  :::{/cell}
  :::{.cell}
  data type name
  :::{/cell}
  :::{.cell}
  `integer`
  :::{/cell}
  :::{/row}
:::{/table}

  : Object Identifier Types

All of the OID alias types for objects that are grouped by namespace accept schema-qualified names, and will display schema-qualified names on output if the object would not be found in the current search path without being qualified. For example, `myschema.mytable` is acceptable input for `regclass` (if there is such a table). That value might be output as `myschema.mytable`, or just `mytable`, depending on the current search path. The `regproc` and `regoper` alias types will only accept input names that are unique (not overloaded), so they are of limited use; for most uses `regprocedure` or `regoperator` are more appropriate. For `regoperator`, unary operators are identified by writing `NONE` for the unused operand.

The input functions for these types allow whitespace between tokens, and will fold upper-case letters to lower case, except within double quotes; this is done to make the syntax rules similar to the way object names are written in SQL. Conversely, the output functions will use double quotes if needed to make the output be a valid SQL identifier. For example, the OID of a function named `Foo` (with upper case `F`) taking two integer arguments could be entered as `' "Foo" ( int, integer ) '::regprocedure`. The output would look like `"Foo"(integer,integer)`. Both the function name and the argument type names could be schema-qualified, too.

Many built-in PostgreSQL functions accept the OID of a table, or another kind of database object, and for convenience are declared as taking `regclass` (or the appropriate OID alias type). This means you do not have to look up the object\'s OID by hand, but can just enter its name as a string literal. For example, the `nextval(regclass)` function takes a sequence relation\'s OID, so you could call it like this:

    nextval('foo')              operates on sequence foo
    nextval('FOO')              same as above
    nextval('"Foo"')            operates on sequence Foo
    nextval('myschema.foo')     operates on myschema.foo
    nextval('"myschema".foo')   same as above
    nextval('foo')              searches search path for foo

:::{.callout type="note"}
When you write the argument of such a function as an unadorned literal string, it becomes a constant of type `regclass` (or the appropriate type). Since this is really just an OID, it will track the originally identified object despite later renaming, schema reassignment, etc. This "early binding" behavior is usually desirable for object references in column defaults and views. But sometimes you might want "late binding" where the object reference is resolved at run time. To get late-binding behavior, force the constant to be stored as a `text` constant instead of `regclass`:

    nextval('foo'::text)      foo is looked up at runtime

The `to_regclass()` function and its siblings can also be used to perform run-time lookups. See [System Catalog Information Functions](braised:ref/functions-info#system-catalog-information-functions).
:::

Another practical example of use of `regclass` is to look up the OID of a table listed in the `information_schema` views, which don\'t supply such OIDs directly.
One might for example wish to call the `pg_relation_size()` function, which requires the table OID.
Taking the above rules into account, the correct way to do that is

    SELECT table_schema, table_name,
           pg_relation_size((quote_ident(table_schema) || '.' ||
                             quote_ident(table_name))::regclass)
    FROM information_schema.tables
    WHERE ...

The `quote_ident()` function will take care of double-quoting the identifiers where needed.
The seemingly easier

    SELECT pg_relation_size(table_name)
    FROM information_schema.tables
    WHERE ...

is *not recommended*, because it will fail for tables that are outside your search path or have names that require quoting.

An additional property of most of the OID alias types is the creation of dependencies.
If a constant of one of these types appears in a stored expression (such as a column default expression or view), it creates a dependency on the referenced object.
For example, if a column has a default expression `nextval('my_seq'::regclass)`, PostgreSQL understands that the default expression depends on the sequence `my_seq`, so the system will not let the sequence be dropped without first removing the default expression.
The alternative of `nextval('my_seq'::text)` does not create a dependency. (`regrole` is an exception to this property.
Constants of this type are not allowed in stored expressions.)

Another identifier type used by the system is `xid`, or transaction (abbreviated xact) identifier.
This is the data type of the system columns xmin and xmax.
Transaction identifiers are 32-bit quantities.
In some contexts, a 64-bit variant `xid8` is used.
Unlike `xid` values, `xid8` values increase strictly monotonically and cannot be reused in the lifetime of a database cluster.
See [Transactions and Identifiers](braised:ref/transaction-id) for more details.

A third identifier type used by the system is `cid`, or command identifier.
This is the data type of the system columns cmin and cmax.
Command identifiers are also 32-bit quantities.

A final identifier type used by the system is `tid`, or tuple identifier (row identifier).
This is the data type of the system column ctid.
A tuple ID is a pair (block number, tuple index within block) that identifies the physical location of the row within its table.

(The system columns are further explained in [System Columns](braised:ref/ddl-system-columns).)
