---
title: "K. PostgreSQL Limits"
id: limits
---

# PostgreSQL Limits

Limitations describes various hard limits of PostgreSQL.
However, practical limits, such as performance limitations or available disk space may apply before absolute hard limits are reached.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Item
  :::{/cell}
  :::{.cell}
  Upper Limit
  :::{/cell}
  :::{.cell}
  Comment
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  database size
  :::{/cell}
  :::{.cell}
  unlimited
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  number of databases
  :::{/cell}
  :::{.cell}
  4,294,950,911
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  relations per database
  :::{/cell}
  :::{.cell}
  1,431,650,303
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  relation size
  :::{/cell}
  :::{.cell}
  32 TB
  :::{/cell}
  :::{.cell}
  with the default `BLCKSZ` of 8192 bytes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  rows per table
  :::{/cell}
  :::{.cell}
  limited by the number of tuples that can fit onto 4,294,967,295 pages
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  columns per table
  :::{/cell}
  :::{.cell}
  1,600
  :::{/cell}
  :::{.cell}
  further limited by tuple size fitting on a single page; see note below
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  columns in a result set
  :::{/cell}
  :::{.cell}
  1,664
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  field size
  :::{/cell}
  :::{.cell}
  1 GB
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  indexes per table
  :::{/cell}
  :::{.cell}
  unlimited
  :::{/cell}
  :::{.cell}
  constrained by maximum relations per database
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  columns per index
  :::{/cell}
  :::{.cell}
  32
  :::{/cell}
  :::{.cell}
  can be increased by recompiling PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  partition keys
  :::{/cell}
  :::{.cell}
  32
  :::{/cell}
  :::{.cell}
  can be increased by recompiling PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  identifier length
  :::{/cell}
  :::{.cell}
  63 bytes
  :::{/cell}
  :::{.cell}
  can be increased by recompiling PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  function arguments
  :::{/cell}
  :::{.cell}
  100
  :::{/cell}
  :::{.cell}
  can be increased by recompiling PostgreSQL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  query parameters
  :::{/cell}
  :::{.cell}
  65,535
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
:::{/table}

  : PostgreSQL Limitations

The maximum number of columns for a table is further reduced as the tuple being stored must fit in a single 8192-byte heap page. For example, excluding the tuple header, a tuple made up of 1,600 `int` columns would consume 6400 bytes and could be stored in a heap page, but a tuple of 1,600 `bigint` columns would consume 12800 bytes and would therefore not fit inside a heap page. Variable-length fields of types such as `text`, `varchar`, and `char` can have their values stored out of line in the table\'s TOAST table when the values are large enough to require it. Only an 18-byte pointer must remain inside the tuple in the table\'s heap. For shorter length variable-length fields, either a 4-byte or 1-byte field header is used and the value is stored inside the heap tuple.

Columns that have been dropped from the table also contribute to the maximum column limit. Moreover, although the dropped column values for newly created tuples are internally marked as null in the tuple\'s null bitmap, the null bitmap also occupies space.

Each table can store a theoretical maximum of 2\^32 out-of-line values; see [TOAST](braised:ref/storage-toast) for a detailed discussion of out-of-line storage. This limit arises from the use of a 32-bit OID to identify each such value. The practical limit is significantly less than the theoretical limit, because as the OID space fills up, finding an OID that is still free can become expensive, in turn slowing down INSERT/UPDATE statements. Typically, this is only an issue for tables containing many terabytes of data; partitioning is a possible workaround.
