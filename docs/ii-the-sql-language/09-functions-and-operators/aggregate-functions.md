---
title: "9.21. Aggregate Functions"
id: functions-aggregate
---

## Aggregate Functions

Aggregate functions compute a single result from a set of input values.
The built-in general-purpose aggregate functions are listed in General-Purpose Aggregate Functions while statistical aggregates are in Aggregate Functions for Statistics.
The built-in within-group ordered-set aggregate functions are listed in Ordered-Set Aggregate Functions while the built-in within-group hypothetical-set ones are in Hypothetical-Set Aggregate Functions.
Grouping operations, which are closely related to aggregate functions, are listed in Grouping Operations.
The special syntax considerations for aggregate functions are explained in [Aggregate Expressions](braised:ref/sql-expressions#aggregate-expressions).
Consult [Aggregate Functions](braised:ref/tutorial-agg) for additional introductory information.

Aggregate functions that support Partial Mode are eligible to participate in various optimizations, such as parallel aggregation.

While all aggregates below accept an optional `ORDER BY` clause (as outlined in [Aggregate Expressions](braised:ref/sql-expressions#aggregate-expressions)), the clause has only been added to aggregates whose output is affected by ordering.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{.cell}
   Partial Mode
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `any_value` ( `anyelement` ) *same as input type*                                                                                                                                                                                                                                                      |

   Returns an arbitrary value from the non-null input values.
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `array_agg` ( `anynonarray` `ORDER BY` `input_sort_columns` ) anyarray

   Collects all the input values, including nulls, into an array.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `array_agg` ( `anyarray` `ORDER BY` `input_sort_columns` ) anyarray

   Concatenates all the input arrays into an array of one higher dimension. (The inputs must all have the same dimensionality, and cannot be empty or null.)
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `avg` ( `smallint` ) numeric

   `avg` ( `integer` ) numeric

   `avg` ( `bigint` ) numeric

   `avg` ( `numeric` ) numeric

   `avg` ( `real` ) double precision

   `avg` ( `double precision` ) double precision

   `avg` ( `interval` ) interval

   Computes the average (arithmetic mean) of all the non-null input values.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bit_and` ( `smallint` ) smallint

   `bit_and` ( `integer` ) integer

   `bit_and` ( `bigint` ) bigint

   `bit_and` ( `bit` ) bit

   Computes the bitwise AND of all non-null input values.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bit_or` ( `smallint` ) smallint

   `bit_or` ( `integer` ) integer

   `bit_or` ( `bigint` ) bigint

   `bit_or` ( `bit` ) bit

   Computes the bitwise OR of all non-null input values.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bit_xor` ( `smallint` ) smallint

   `bit_xor` ( `integer` ) integer

   `bit_xor` ( `bigint` ) bigint

   `bit_xor` ( `bit` ) bit

   Computes the bitwise exclusive OR of all non-null input values. Can be useful as a checksum for an unordered set of values.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bool_and` ( `boolean` ) boolean

   Returns true if all non-null input values are true, otherwise false.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bool_or` ( `boolean` ) boolean

   Returns true if any non-null input value is true, otherwise false.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `count` ( `*` ) bigint

   Computes the number of input rows.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `count` ( `"any"` ) bigint

   Computes the number of input rows in which the input value is not null.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `every` ( `boolean` ) boolean

   This is the SQL standard\'s equivalent to `bool_and`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_agg` ( `anyelement` `ORDER BY` `input_sort_columns` ) json

   `jsonb_agg` ( `anyelement` `ORDER BY` `input_sort_columns` ) jsonb

   Collects all the input values, including nulls, into a JSON array. Values are converted to JSON as per `to_json` or `to_jsonb`.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_agg_strict` ( `anyelement` ) json

   `jsonb_agg_strict` ( `anyelement` ) jsonb

   Collects all the input values, skipping nulls, into a JSON array. Values are converted to JSON as per `to_json` or `to_jsonb`.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_arrayagg` ( \[*value_expression*\] \[`ORDER BY` *sort_expression*\] \[{ `NULL` \| `ABSENT` } `ON NULL`\] \[`RETURNING` *data_type* \[`FORMAT JSON` \[`ENCODING UTF8`\]\]\])                                                                                                                  | No

   Behaves in the same way as `json_array` but as an aggregate function so it only takes one *value_expression* parameter. If `ABSENT ON NULL` is specified, any NULL values are omitted. If `ORDER BY` is specified, the elements will appear in the array in that order rather than in the input order. |

   `SELECT json_arrayagg(v) FROM (VALUES(2),(1)) t(v)` \[2, 1\]
  :::{/cell}
  :::{.cell}
          |

              |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_objectagg` ( \[{ *key_expression* { `VALUE` \| \':\' } *value_expression* }\] \[{ `NULL` \| `ABSENT` } `ON NULL`\] \[{ `WITH` \| `WITHOUT` } `UNIQUE` \[`KEYS`\]\] \[`RETURNING` *data_type* \[`FORMAT JSON` \[`ENCODING UTF8`\]\]\])                                                        | No

   Behaves like `json_object`, but as an aggregate function, so it only takes one *key_expression* and one *value_expression* parameter.                                                                                                                                                                |

   `SELECT json_objectagg(k:v) FROM (VALUES ('a'::text,current_date),('b',current_date + 1)) AS t(k,v)` { \"a\" : \"2022-05-10\", \"b\" : \"2022-05-11\" }
  :::{/cell}
  :::{.cell}
          |

            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_object_agg` ( `key` `"any"`, `value` `"any"` `ORDER BY` `input_sort_columns` ) json

   `jsonb_object_agg` ( `key` `"any"`, `value` `"any"` `ORDER BY` `input_sort_columns` ) jsonb

   Collects all the key/value pairs into a JSON object. Key arguments are coerced to text; value arguments are converted as per `to_json` or `to_jsonb`. Values can be null, but keys cannot.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_object_agg_strict` ( `key` `"any"`, `value` `"any"` ) json

   `jsonb_object_agg_strict` ( `key` `"any"`, `value` `"any"` ) jsonb

   Collects all the key/value pairs into a JSON object. Key arguments are coerced to text; value arguments are converted as per `to_json` or `to_jsonb`. The `key` can not be null. If the `value` is null then the entry is skipped,
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_object_agg_unique` ( `key` `"any"`, `value` `"any"` ) json

   `jsonb_object_agg_unique` ( `key` `"any"`, `value` `"any"` ) jsonb

   Collects all the key/value pairs into a JSON object. Key arguments are coerced to text; value arguments are converted as per `to_json` or `to_jsonb`. Values can be null, but keys cannot. If there is a duplicate key an error is thrown.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `json_object_agg_unique_strict` ( `key` `"any"`, `value` `"any"` ) json

   `jsonb_object_agg_unique_strict` ( `key` `"any"`, `value` `"any"` ) jsonb

   Collects all the key/value pairs into a JSON object. Key arguments are coerced to text; value arguments are converted as per `to_json` or `to_jsonb`. The `key` can not be null. If the `value` is null then the entry is skipped. If there is a duplicate key an error is thrown.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `max` ( *see text* ) *same as input type*                                                                                                                                                                                                                                                            | Ye

   Computes the maximum of the non-null input values. Available for any numeric, string, date/time, or enum type, as well as `bytea`, `inet`, `interval`, `money`, `oid`, `pg_lsn`, `tid`, `xid8`, and also arrays and composite types containing sortable data types.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `min` ( *see text* ) *same as input type*                                                                                                                                                                                                                                                            | Ye

   Computes the minimum of the non-null input values. Available for any numeric, string, date/time, or enum type, as well as `bytea`, `inet`, `interval`, `money`, `oid`, `pg_lsn`, `tid`, `xid8`, and also arrays and composite types containing sortable data types.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `range_agg` ( `value` `anyrange` ) anymultirange

   `range_agg` ( `value` `anymultirange` ) anymultirange

   Computes the union of the non-null input values.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `range_intersect_agg` ( `value` `anyrange` ) anyrange

   `range_intersect_agg` ( `value` `anymultirange` ) anymultirange

   Computes the intersection of the non-null input values.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `string_agg` ( `value` `text`, `delimiter` `text` ) text

   `string_agg` ( `value` `bytea`, `delimiter` `bytea` `ORDER BY` `input_sort_columns` ) bytea

   Concatenates the non-null input values into a string. Each value after the first is preceded by the corresponding `delimiter` (if it\'s not null).
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sum` ( `smallint` ) bigint

   `sum` ( `integer` ) bigint

   `sum` ( `bigint` ) numeric

   `sum` ( `numeric` ) numeric

   `sum` ( `real` ) real

   `sum` ( `double precision` ) double precision

   `sum` ( `interval` ) interval

   `sum` ( `money` ) money

   Computes the sum of the non-null input values.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `xmlagg` ( `xml` `ORDER BY` `input_sort_columns` ) xml

   Concatenates the non-null XML input values (see [xmlagg](braised:ref/functions-xml#xmlagg)).
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
:::{/table}

: General-Purpose Aggregate Functions

It should be noted that except for `count`, these functions return a null value when no rows are selected. In particular, `sum` of no rows returns null, not zero as one might expect, and `array_agg` returns null rather than an empty array when there are no input rows. The `coalesce` function can be used to substitute zero or an empty array for null when necessary.

The aggregate functions `array_agg`, `json_agg`, `jsonb_agg`, `json_agg_strict`, `jsonb_agg_strict`, `json_object_agg`, `jsonb_object_agg`, `json_object_agg_strict`, `jsonb_object_agg_strict`, `json_object_agg_unique`, `jsonb_object_agg_unique`, `json_object_agg_unique_strict`, `jsonb_object_agg_unique_strict`, `string_agg`, and `xmlagg`, as well as similar user-defined aggregate functions, produce meaningfully different result values depending on the order of the input values. This ordering is unspecified by default, but can be controlled by writing an `ORDER BY` clause within the aggregate call, as shown in [Aggregate Expressions](braised:ref/sql-expressions#aggregate-expressions). Alternatively, supplying the input values from a sorted subquery will usually work. For example:

    SELECT xmlagg(x) FROM (SELECT x FROM test ORDER BY y DESC) AS tab;

Beware that this approach can fail if the outer query level contains additional processing, such as a join, because that might cause the subquery\'s output to be reordered before the aggregate is computed.

:::{.callout type="note"}
The boolean aggregates `bool_and` and `bool_or` correspond to the standard SQL aggregates `every` and `any` or `some`. PostgreSQL supports `every`, but not `any` or `some`, because there is an ambiguity built into the standard syntax:

    SELECT b1 = ANY((SELECT b2 FROM t2 ...)) FROM t1 ...;

Here `ANY` can be considered either as introducing a subquery, or as being an aggregate function, if the subquery returns one row with a Boolean value. Thus the standard name cannot be given to these aggregates.
:::

:::{.callout type="note"}
Users accustomed to working with other SQL database management systems might be disappointed by the performance of the `count` aggregate when it is applied to the entire table. A query like:

    SELECT count(*) FROM sometable;

will require effort proportional to the size of the table: PostgreSQL will need to scan either the entire table or the entirety of an index that includes all rows in the table.
:::

Aggregate Functions for Statistics shows aggregate functions typically used in statistical analysis. (These are separated out merely to avoid cluttering the listing of more-commonly-used aggregates.) Functions shown as accepting *numeric_type* are available for all the types `smallint`, `integer`, `bigint`, `numeric`, `real`, and `double precision`.
Where the description mentions `N`, it means the number of input rows for which all the input expressions are non-null.
In all cases, null is returned if the computation is meaningless, for example when `N` is zero.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{.cell}
   Partial Mode
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `corr` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the correlation coefficient.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `covar_pop` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the population covariance.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `covar_samp` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the sample covariance.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_avgx` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the average of the independent variable, `sum(X)/N`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_avgy` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the average of the dependent variable, `sum(Y)/N`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_count` ( `Y` `double precision`, `X` `double precision` ) bigint

   Computes the number of rows in which both inputs are non-null.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_intercept` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the y-intercept of the least-squares-fit linear equation determined by the (`X`, `Y`) pairs.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_r2` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the square of the correlation coefficient.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_slope` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the slope of the least-squares-fit linear equation determined by the (`X`, `Y`) pairs.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_sxx` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the "sum of squares" of the independent variable, `sum(X^2) - sum(X)^2/N`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_sxy` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the "sum of products" of independent times dependent variables, `sum(X*Y) - sum(X) * sum(Y)/N`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `regr_syy` ( `Y` `double precision`, `X` `double precision` ) double precision

   Computes the "sum of squares" of the dependent variable, `sum(Y^2) - sum(Y)^2/N`.
  :::{/cell}
  :::{.cell}
   Yes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `stddev` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric`      |

   This is a historical alias for `stddev_samp`.
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `stddev_pop` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric`  |

   Computes the population standard deviation of the input values.
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `stddev_samp` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric` |

   Computes the sample standard deviation of the input values.
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `variance` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric`    |

   This is a historical alias for `var_samp`.
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `var_pop` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric`     |

   Computes the population variance of the input values (square of the population standard deviation).
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `var_samp` ( *numeric_type* ) `double precision` for `real` or `double precision`, otherwise `numeric`    |

   Computes the sample variance of the input values (square of the sample standard deviation).
  :::{/cell}
  :::{.cell}
  es          |
  :::{/cell}
  :::{/row}
:::{/table}

: Aggregate Functions for Statistics

Ordered-Set Aggregate Functions shows some aggregate functions that use the ordered-set aggregate syntax. These functions are sometimes referred to as "inverse distribution" functions. Their aggregated input is introduced by `ORDER BY`, and they may also take a direct argument that is not aggregated, but is computed only once. All these functions ignore null values in their aggregated input. For those that take a `fraction` parameter, the fraction value must be between 0 and 1; an error is thrown if not. However, a null `fraction` value simply produces a null result.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{.cell}
   Partial Mode
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `mode` () `WITHIN GROUP` ( `ORDER BY` `anyelement` ) anyelement

   Computes the mode, the most frequent value of the aggregated argument (arbitrarily choosing the first one if there are multiple equally-frequent values). The aggregated argument must be of a sortable type.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `percentile_cont` ( `fraction` `double precision` ) `WITHIN GROUP` ( `ORDER BY` `double precision` ) double precision

   `percentile_cont` ( `fraction` `double precision` ) `WITHIN GROUP` ( `ORDER BY` `interval` ) interval

   Computes the continuous percentile, a value corresponding to the specified `fraction` within the ordered set of aggregated argument values. This will interpolate between adjacent input items if needed.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `percentile_cont` ( `fractions` `double precision[]` ) `WITHIN GROUP` ( `ORDER BY` `double precision` ) double precision\[\]

   `percentile_cont` ( `fractions` `double precision[]` ) `WITHIN GROUP` ( `ORDER BY` `interval` ) interval\[\]

   Computes multiple continuous percentiles. The result is an array of the same dimensions as the `fractions` parameter, with each non-null element replaced by the (possibly interpolated) value corresponding to that percentile.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `percentile_disc` ( `fraction` `double precision` ) `WITHIN GROUP` ( `ORDER BY` `anyelement` ) anyelement

   Computes the discrete percentile, the first value within the ordered set of aggregated argument values whose position in the ordering equals or exceeds the specified `fraction`. The aggregated argument must be of a sortable type.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `percentile_disc` ( `fractions` `double precision[]` ) `WITHIN GROUP` ( `ORDER BY` `anyelement` ) anyarray

   Computes multiple discrete percentiles. The result is an array of the same dimensions as the `fractions` parameter, with each non-null element replaced by the input value corresponding to that percentile. The aggregated argument must be of a sortable type.
  :::{/cell}
  :::{.cell}
   No
  :::{/cell}
  :::{/row}
:::{/table}

: Ordered-Set Aggregate Functions

Each of the "hypothetical-set" aggregates listed in Hypothetical-Set Aggregate Functions is associated with a window function of the same name defined in [Window Functions](braised:ref/functions-window). In each case, the aggregate\'s result is the value that the associated window function would have returned for the "hypothetical" row constructed from *args*, if such a row had been added to the sorted group of rows represented by the *sorted_args*. For each of these functions, the list of direct arguments given in *args* must match the number and types of the aggregated arguments given in *sorted_args*. Unlike most built-in aggregates, these aggregates are not strict, that is they do not drop input rows containing nulls. Null values sort according to the rule specified in the `ORDER BY` clause.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{.cell}
   Partial Mode
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `rank` ( *args* ) `WITHIN GROUP` ( `ORDER BY` *sorted_args* ) bigint                                                                                       | No

   Computes the rank of the hypothetical row, with gaps; that is, the row number of the first row in its peer group.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `dense_rank` ( *args* ) `WITHIN GROUP` ( `ORDER BY` *sorted_args* ) bigint                                                                                 | No

   Computes the rank of the hypothetical row, without gaps; this function effectively counts peer groups.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `percent_rank` ( *args* ) `WITHIN GROUP` ( `ORDER BY` *sorted_args* ) double precision                                                                     | No

   Computes the relative rank of the hypothetical row, that is (`rank` - 1) / (total rows - 1). The value thus ranges from 0 to 1 inclusive.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `cume_dist` ( *args* ) `WITHIN GROUP` ( `ORDER BY` *sorted_args* ) double precision                                                                        | No

   Computes the cumulative distribution, that is (number of rows preceding or peers with hypothetical row) / (total rows). The value thus ranges from 1/`N` to 1.
  :::{/cell}
  :::{.cell}
            |
  :::{/cell}
  :::{/row}
:::{/table}

: Hypothetical-Set Aggregate Functions

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `GROUPING` ( *group_by_expression(s)* ) integer                                                                                                                                                                                                                                                                                                                         |

   Returns a bit mask indicating which `GROUP BY` expressions are not included in the current grouping set. Bits are assigned with the rightmost argument corresponding to the least-significant bit; each bit is 0 if the corresponding expression is included in the grouping criteria of the grouping set generating the current result row, and 1 if it is not included.
  :::{/cell}
  :::{/row}
:::{/table}

: Grouping Operations

The grouping operations shown in Grouping Operations are used in conjunction with grouping sets (see [GROUPING SETS, CUBE, and ROLLUP](braised:ref/queries-table-expressions#grouping-sets-cube-and-rollup)) to distinguish result rows. The arguments to the `GROUPING` function are not actually evaluated, but they must exactly match expressions given in the `GROUP BY` clause of the associated query level. For example:

    => SELECT * FROM items_sold;
     make  | model | sales
    -------+-------+-------
     Foo   | GT    |  10
     Foo   | Tour  |  20
     Bar   | City  |  15
     Bar   | Sport |  5
    (4 rows)

    => SELECT make, model, GROUPING(make,model), sum(sales) FROM items_sold GROUP BY ROLLUP(make,model);
     make  | model | grouping | sum
    -------+-------+----------+-----
     Foo   | GT    |        0 | 10
     Foo   | Tour  |        0 | 20
     Bar   | City  |        0 | 15
     Bar   | Sport |        0 | 5
     Foo   |       |        1 | 30
     Bar   |       |        1 | 20
           |       |        3 | 50
    (7 rows)

Here, the `grouping` value `0` in the first four rows shows that those have been grouped normally, over both the grouping columns. The value `1` indicates that `model` was not grouped by in the next-to-last two rows, and the value `3` indicates that neither `make` nor `model` was grouped by in the last row (which therefore is an aggregate over all the input rows).
