---
title: "65.5. BRIN Indexes"
id: brin
---

## BRIN Indexes

### Introduction

BRIN stands for Block Range Index.
BRIN is designed for handling very large tables in which certain columns have some natural correlation with their physical location within the table.

BRIN works in terms of block ranges (or "page ranges").
A block range is a group of pages that are physically adjacent in the table; for each block range, some summary info is stored by the index.
For example, a table storing a store\'s sale orders might have a date column on which each order was placed, and most of the time the entries for earlier orders will appear earlier in the table as well; a table storing a ZIP code column might have all codes for a city grouped together naturally.

BRIN indexes can satisfy queries via regular bitmap index scans, and will return all tuples in all pages within each range if the summary info stored by the index is consistent with the query conditions.
The query executor is in charge of rechecking these tuples and discarding those that do not match the query conditions in other words, these indexes are lossy.
Because a BRIN index is very small, scanning the index adds little overhead compared to a sequential scan, but may avoid scanning large parts of the table that are known not to contain matching tuples.

The specific data that a BRIN index will store, as well as the specific queries that the index will be able to satisfy, depend on the operator class selected for each column of the index.
Data types having a linear sort order can have operator classes that store the minimum and maximum value within each block range, for instance; geometrical types might store the bounding box for all the objects in the block range.

The size of the block range is determined at index creation time by the `pages_per_range` storage parameter.
The number of index entries will be equal to the size of the relation in pages divided by the selected value for `pages_per_range`.
Therefore, the smaller the number, the larger the index becomes (because of the need to store more index entries), but at the same time the summary data stored can be more precise and more data blocks can be skipped during an index scan.

#### Index Maintenance

At the time of creation, all existing heap pages are scanned and a summary index tuple is created for each range, including the possibly-incomplete range at the end.
As new pages are filled with data, page ranges that are already summarized will cause the summary information to be updated with data from the new tuples.
When a new page is created that does not fall within the last summarized range, the range that the new page belongs to does not automatically acquire a summary tuple; those tuples remain unsummarized until a summarization run is invoked later, creating the initial summary for that range.

There are several ways to trigger the initial summarization of a page range.
If the table is vacuumed, either manually or by [autovacuum](#autovacuum), all existing unsummarized page ranges are summarized.
Also, if the index\'s [autosummarize (boolean)
     
      autosummarize storage parameter](braised:ref/sql-createindex#autosummarize-boolean-autosummarize-storage-parameter) parameter is enabled, which it isn\'t by default, whenever autovacuum runs in that database, summarization will occur for all unsummarized page ranges that have been filled, regardless of whether the table itself is processed by autovacuum; see below.

Lastly, the following functions can be used (while these functions run, [search_path (string)
      
       search_path configuration parameter
      
      pathfor schemas](braised:ref/runtime-config-client#search-path-string-search-path-configuration-parameter-pathfor-schemas) is temporarily changed to `pg_catalog, pg_temp`): `brin_summarize_new_values(regclass)` which summarizes all unsummarized ranges;, `brin_summarize_range(regclass, bigint)` which summarizes only the range containing the given page, if it is unsummarized.

When autosummarization is enabled, a request is sent to `autovacuum` to execute a targeted summarization for a block range when an insertion is detected for the first item of the first page of the next block range, to be fulfilled the next time an autovacuum worker finishes running in the same database.
If the request queue is full, the request is not recorded and a message is sent to the server log:

    LOG:  request for BRIN range summarization for index "brin_wi_idx" page 128 was not recorded

When this happens, the range will remain unsummarized until the next regular vacuum run on the table, or one of the functions mentioned above are invoked.

Conversely, a range can be de-summarized using the `brin_desummarize_range(regclass, bigint)` function, which is useful when the index tuple is no longer a very good representation because the existing values have changed.
See [Index Maintenance Functions](braised:ref/functions-admin#index-maintenance-functions) for details.

### Built-in Operator Classes

The core PostgreSQL distribution includes the BRIN operator classes shown in Built-in Operator Classes.

The minmax operator classes store the minimum and the maximum values appearing in the indexed column within the range.
The inclusion operator classes store a value which includes the values in the indexed column within the range.
The bloom operator classes build a Bloom filter for all values in the range.
The minmax-multi operator classes store multiple minimum and maximum values, representing values appearing in the indexed column within the range.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Indexable Operators
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bit_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (bit,bit)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (bit,bit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (bit,bit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (bit,bit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (bit,bit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `box_inclusion_ops`
  :::{/cell}
  :::{.cell}
  `@> (box,point)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<< (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&< (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&> (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>> (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<@ (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `@> (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `~= (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&& (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<<| (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&<| (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `|&> (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `|>> (box,box)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bpchar_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (character,character)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bpchar_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (character,character)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (character,character)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (character,character)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (character,character)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (character,character)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bytea_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (bytea,bytea)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `bytea_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (bytea,bytea)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (bytea,bytea)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (bytea,bytea)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (bytea,bytea)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (bytea,bytea)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `char_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= ("char","char")`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `char_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= ("char","char")`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< ("char","char")`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= ("char","char")`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> ("char","char")`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= ("char","char")`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `date_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (date,date)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `date_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (date,date)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `date_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (date,date)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (date,date)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float4_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (float4,float4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float4_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (float4,float4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float4_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (float4,float4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (float4,float4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float8_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (float8,float8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float8_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (float8,float8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `float8_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (float8,float8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (float8,float8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `inet_inclusion_ops`
  :::{/cell}
  :::{.cell}
  `<< (inet,inet)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<<= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>> (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>>= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&& (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `inet_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (inet,inet)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `inet_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (inet,inet)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `inet_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (inet,inet)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (inet,inet)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int2_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (int2,int2)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int2_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (int2,int2)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int2_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (int2,int2)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (int2,int2)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int4_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (int4,int4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int4_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (int4,int4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int4_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (int4,int4)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (int4,int4)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int8_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (bigint,bigint)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int8_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (bigint,bigint)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `int8_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (bigint,bigint)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (bigint,bigint)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `interval_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (interval,interval)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `interval_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (interval,interval)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `interval_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (interval,interval)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (interval,interval)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr,macaddr)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr,macaddr)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr,macaddr)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (macaddr,macaddr)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr8_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr8,macaddr8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr8_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr8,macaddr8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `macaddr8_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (macaddr8,macaddr8)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (macaddr8,macaddr8)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `name_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (name,name)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `name_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (name,name)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (name,name)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (name,name)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (name,name)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (name,name)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `numeric_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (numeric,numeric)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `numeric_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (numeric,numeric)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `numeric_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (numeric,numeric)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (numeric,numeric)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `oid_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (oid,oid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `oid_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (oid,oid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `oid_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (oid,oid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (oid,oid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `pg_lsn_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `pg_lsn_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `pg_lsn_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (pg_lsn,pg_lsn)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `range_inclusion_ops`
  :::{/cell}
  :::{.cell}
  `= (anyrange,anyrange)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&& (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `@> (anyrange,anyelement)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `@> (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<@ (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<< (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>> (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&< (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `&> (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `-|- (anyrange,anyrange)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `text_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (text,text)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `text_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (text,text)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (text,text)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (text,text)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (text,text)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (text,text)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `tid_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (tid,tid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `tid_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (tid,tid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `tid_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (tid,tid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (tid,tid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamp_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamp,timestamp)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamp_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamp,timestamp)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamp_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamp,timestamp)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timestamp,timestamp)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamptz_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamptz,timestamptz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamptz_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamptz,timestamptz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timestamptz_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (timestamptz,timestamptz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timestamptz,timestamptz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `time_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (time,time)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `time_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (time,time)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `time_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (time,time)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (time,time)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timetz_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (timetz,timetz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timetz_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (timetz,timetz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `timetz_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (timetz,timetz)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (timetz,timetz)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `uuid_bloom_ops`
  :::{/cell}
  :::{.cell}
  `= (uuid,uuid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `uuid_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (uuid,uuid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `uuid_minmax_multi_ops`
  :::{/cell}
  :::{.cell}
  `= (uuid,uuid)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (uuid,uuid)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `varbit_minmax_ops`
  :::{/cell}
  :::{.cell}
  `= (varbit,varbit)`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `< (varbit,varbit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `> (varbit,varbit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `<= (varbit,varbit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `>= (varbit,varbit)`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
:::{/table}

  : Built-in BRIN Operator Classes

#### Operator Class Parameters

Some of the built-in operator classes allow specifying parameters affecting behavior of the operator class. Each operator class has its own set of allowed parameters. Only the `bloom` and `minmax-multi` operator classes allow specifying parameters:

bloom operator classes accept these parameters:

:::{.dl}
:::{.item term="`n_distinct_per_range`"}
Defines the estimated number of distinct non-null values in the block range, used by BRIN bloom indexes for sizing of the Bloom filter. It behaves similarly to `n_distinct` option for [ALTER TABLE](braised:ref/sql-altertable). When set to a positive value, each block range is assumed to contain this number of distinct non-null values. When set to a negative value, which must be greater than or equal to -1, the number of distinct non-null values is assumed to grow linearly with the maximum possible number of tuples in the block range (about 290 rows per block). The default value is `-0.1`, and the minimum number of distinct non-null values is `16`.
:::{/item}
:::{.item term="`false_positive_rate`"}
Defines the desired false positive rate used by BRIN bloom indexes for sizing of the Bloom filter. The values must be between 0.0001 and 0.25. The default value is 0.01, which is 1% false positive rate.
:::{/item}
:::{/dl}

minmax-multi operator classes accept these parameters:

:::{.dl}
:::{.item term="`values_per_range`"}
Defines the maximum number of values stored by BRIN minmax indexes to summarize a block range. Each value may represent either a point, or a boundary of an interval. Values must be between 8 and 256, and the default value is 32.
:::{/item}
:::{/dl}

### Extensibility

The BRIN interface has a high level of abstraction, requiring the access method implementer only to implement the semantics of the data type being accessed. The BRIN layer itself takes care of concurrency, logging and searching the index structure.

All it takes to get a BRIN access method working is to implement a few user-defined methods, which define the behavior of summary values stored in the index and the way they interact with scan keys. In short, BRIN combines extensibility with generality, code reuse, and a clean interface.

There are four methods that an operator class for BRIN must provide:

:::{.dl}
:::{.item term="`BrinOpcInfo *opcInfo(Oid type_oid)`"}
Returns internal information about the indexed columns\' summary data. The return value must point to a palloc\'d BrinOpcInfo, which has this definition:

    typedef struct BrinOpcInfo
    {
        /* Number of columns stored in an index column of this opclass */
        uint16      oi_nstored;

        /* Opaque pointer for the opclass' private use */
        void       *oi_opaque;

        /* Type cache entries of the stored columns */
        TypeCacheEntry *oi_typcache[FLEXIBLE_ARRAY_MEMBER];
    } BrinOpcInfo;

BrinOpcInfo.oi_opaque can be used by the operator class routines to pass information between support functions during an index scan.
:::{/item}
:::{.item term="`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey *keys, int nkeys)`"}
Returns whether all the ScanKey entries are consistent with the given indexed values for a range. The attribute number to use is passed as part of the scan key. Multiple scan keys for the same attribute may be passed at once; the number of entries is determined by the `nkeys` parameter.
:::{/item}
:::{.item term="`bool consistent(BrinDesc *bdesc, BrinValues *column, ScanKey key)`"}
Returns whether the ScanKey is consistent with the given indexed values for a range. The attribute number to use is passed as part of the scan key. This is an older backward-compatible variant of the consistent function.
:::{/item}
:::{.item term="`bool addValue(BrinDesc *bdesc, BrinValues *column, Datum newval, bool isnull)`"}
Given an index tuple and an indexed value, modifies the indicated attribute of the tuple so that it additionally represents the new value. If any modification was done to the tuple, `true` is returned.
:::{/item}
:::{.item term="`bool unionTuples(BrinDesc *bdesc, BrinValues *a, BrinValues *b)`"}
Consolidates two index tuples. Given two index tuples, modifies the indicated attribute of the first of them so that it represents both tuples. The second tuple is not modified.
:::{/item}
:::{/dl}

An operator class for BRIN can optionally specify the following method:

:::{.dl}
:::{.item term="`void options(local_relopts *relopts)`"}
Defines a set of user-visible parameters that control operator class behavior.

The `options` function is passed a pointer to a local_relopts struct, which needs to be filled with a set of operator class specific options. The options can be accessed from other support functions using the `PG_HAS_OPCLASS_OPTIONS()` and `PG_GET_OPCLASS_OPTIONS()` macros.

Since both key extraction of indexed values and representation of the key in BRIN are flexible, they may depend on user-specified parameters.
:::{/item}
:::{/dl}

The core distribution includes support for four types of operator classes: minmax, minmax-multi, inclusion and bloom. Operator class definitions using them are shipped for in-core data types as appropriate. Additional operator classes can be defined by the user for other data types using equivalent definitions, without having to write any source code; appropriate catalog entries being declared is enough. Note that assumptions about the semantics of operator strategies are embedded in the support functions\' source code.

Operator classes that implement completely different semantics are also possible, provided implementations of the four main support functions described above are written. Note that backwards compatibility across major releases is not guaranteed: for example, additional support functions might be required in later releases.

To write an operator class for a data type that implements a totally ordered set, it is possible to use the minmax support functions alongside the corresponding operators, as shown in Function and Support Numbers for Minmax Operator Classes. All operator class members (functions and operators) are mandatory.

  -----------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Operator class member
  :::{/cell}
  :::{.cell}
  Object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Function 1
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_opcinfo()`
  :::{/cell}
  :::{/row}
:::{/table}

  Support Function 2      internal function `brin_minmax_add_value()`

  Support Function 3      internal function `brin_minmax_consistent()`

  Support Function 4      internal function `brin_minmax_union()`

  Operator Strategy 1     operator less-than

  Operator Strategy 2     operator less-than-or-equal-to

  Operator Strategy 3     operator equal-to

  Operator Strategy 4     operator greater-than-or-equal-to

  Operator Strategy 5     operator greater-than
  -----------------------------------------------------------------------

  : Function and Support Numbers for Minmax Operator Classes

To write an operator class for a complex data type which has values included within another type, it\'s possible to use the inclusion support functions alongside the corresponding operators, as shown in Function and Support Numbers for Inclusion Operator Classes. It requires only a single additional function, which can be written in any language. More functions can be defined for additional functionality. All operators are optional. Some operators require other operators, as shown as dependencies on the table.

  -------------------------------------------------------------------------------------------------------------------------------
:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Operator class member
  :::{/cell}
  :::{.cell}
  Object
  :::{/cell}
  :::{.cell}
  Dependency
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Function 1
  :::{/cell}
  :::{.cell}
  internal function `brin_inclusion_opcinfo()`
  :::{/cell}
  :::{.cell}
  :::{/cell}
  :::{/row}
:::{/table}

  Support Function 2                internal function `brin_inclusion_add_value()`                         

  Support Function 3                internal function `brin_inclusion_consistent()`                        

  Support Function 4                internal function `brin_inclusion_union()`                             

  Support Function 11               function to merge two elements                                         

  Support Function 12               optional function to check whether two elements are mergeable          

  Support Function 13               optional function to check if an element is contained within another   

  Support Function 14               optional function to check whether an element is empty                 

  Operator Strategy 1               operator left-of                                                       Operator Strategy 4

  Operator Strategy 2               operator does-not-extend-to-the-right-of                               Operator Strategy 5

  Operator Strategy 3               operator overlaps                                                      

  Operator Strategy 4               operator does-not-extend-to-the-left-of                                Operator Strategy 1

  Operator Strategy 5               operator right-of                                                      Operator Strategy 2

  Operator Strategy 6, 18           operator same-as-or-equal-to                                           Operator Strategy 7

  Operator Strategy 7, 16, 24, 25   operator contains-or-equal-to                                          

  Operator Strategy 8, 26, 27       operator is-contained-by-or-equal-to                                   Operator Strategy 3

  Operator Strategy 9               operator does-not-extend-above                                         Operator Strategy 11

  Operator Strategy 10              operator is-below                                                      Operator Strategy 12

  Operator Strategy 11              operator is-above                                                      Operator Strategy 9

  Operator Strategy 12              operator does-not-extend-below                                         Operator Strategy 10

  Operator Strategy 20              operator less-than                                                     Operator Strategy 5

  Operator Strategy 21              operator less-than-or-equal-to                                         Operator Strategy 5

  Operator Strategy 22              operator greater-than                                                  Operator Strategy 1

  Operator Strategy 23              operator greater-than-or-equal-to                                      Operator Strategy 1
  -------------------------------------------------------------------------------------------------------------------------------

  : Function and Support Numbers for Inclusion Operator Classes

Support function numbers 1 through 10 are reserved for the BRIN internal functions, so the SQL level functions start with number 11. Support function number 11 is the main function required to build the index. It should accept two arguments with the same data type as the operator class, and return the union of them. The inclusion operator class can store union values with different data types if it is defined with the `STORAGE` parameter. The return value of the union function should match the `STORAGE` data type.

Support function numbers 12 and 14 are provided to support irregularities of built-in data types. Function number 12 is used to support network addresses from different families which are not mergeable. Function number 14 is used to support empty ranges. Function number 13 is an optional but recommended one, which allows the new value to be checked before it is passed to the union function. As the BRIN framework can shortcut some operations when the union is not changed, using this function can improve index performance.

To write an operator class for a data type that implements only an equality operator and supports hashing, it is possible to use the bloom support procedures alongside the corresponding operators, as shown in Procedure and Support Numbers for Bloom Operator Classes. All operator class members (procedures and operators) are mandatory.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Operator class member
  :::{/cell}
  :::{.cell}
  Object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 1
  :::{/cell}
  :::{.cell}
  internal function `brin_bloom_opcinfo()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 2
  :::{/cell}
  :::{.cell}
  internal function `brin_bloom_add_value()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 3
  :::{/cell}
  :::{.cell}
  internal function `brin_bloom_consistent()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 4
  :::{/cell}
  :::{.cell}
  internal function `brin_bloom_union()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 5
  :::{/cell}
  :::{.cell}
  internal function `brin_bloom_options()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 11
  :::{/cell}
  :::{.cell}
  function to compute hash of an element
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 1
  :::{/cell}
  :::{.cell}
  operator equal-to
  :::{/cell}
  :::{/row}
:::{/table}

  : Procedure and Support Numbers for Bloom Operator Classes

Support procedure numbers 1-10 are reserved for the BRIN internal functions, so the SQL level functions start with number 11. Support function number 11 is the main function required to build the index. It should accept one argument with the same data type as the operator class, and return a hash of the value.

The minmax-multi operator class is also intended for data types implementing a totally ordered set, and may be seen as a simple extension of the minmax operator class. While minmax operator class summarizes values from each block range into a single contiguous interval, minmax-multi allows summarization into multiple smaller intervals to improve handling of outlier values. It is possible to use the minmax-multi support procedures alongside the corresponding operators, as shown in Procedure and Support Numbers for minmax-multi Operator Classes. All operator class members (procedures and operators) are mandatory.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Operator class member
  :::{/cell}
  :::{.cell}
  Object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 1
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_multi_opcinfo()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 2
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_multi_add_value()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 3
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_multi_consistent()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 4
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_multi_union()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 5
  :::{/cell}
  :::{.cell}
  internal function `brin_minmax_multi_options()`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Support Procedure 11
  :::{/cell}
  :::{.cell}
  function to compute distance between two values (length of a range)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 1
  :::{/cell}
  :::{.cell}
  operator less-than
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 2
  :::{/cell}
  :::{.cell}
  operator less-than-or-equal-to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 3
  :::{/cell}
  :::{.cell}
  operator equal-to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 4
  :::{/cell}
  :::{.cell}
  operator greater-than-or-equal-to
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  Operator Strategy 5
  :::{/cell}
  :::{.cell}
  operator greater-than
  :::{/cell}
  :::{/row}
:::{/table}

  : Procedure and Support Numbers for minmax-multi Operator Classes

Both minmax and inclusion operator classes support cross-data-type operators, though with these the dependencies become more complicated. The minmax operator class requires a full set of operators to be defined with both arguments having the same data type. It allows additional data types to be supported by defining extra sets of operators. Inclusion operator class operator strategies are dependent on another operator strategy as shown in Function and Support Numbers for Inclusion Operator Classes, or the same operator strategy as themselves. They require the dependency operator to be defined with the `STORAGE` data type as the left-hand-side argument and the other supported data type to be the right-hand-side argument of the supported operator. See `float4_minmax_ops` as an example of minmax, and `box_inclusion_ops` as an example of inclusion.
