---
title: "52.39. pg_proc"
id: catalog-pg-proc
---

## pg_proc

The catalog pg_proc stores information about functions, procedures, aggregate functions, and window functions (collectively also known as routines).
See [CREATE FUNCTION](braised:ref/sql-createfunction), [CREATE PROCEDURE](braised:ref/sql-createprocedure), and [User-Defined Functions](braised:ref/xfunc) for more information.

If prokind indicates that the entry is for an aggregate function, there should be a matching row in [pg_aggregate](#catalog-pg-aggregate).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proname `name`

   Name of the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pronamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prolang `oid` (references [pg_language](#catalog-pg-language).oid)

   Implementation language or call interface of this function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   procost `float4`

   Estimated execution cost (in units of [cpu_operator_cost (floating point)
      
       cpu_operator_cost configuration parameter](braised:ref/runtime-config-query#cpu-operator-cost-floating-point-cpu-operator-cost-configuration-parameter)); if proretset, this is cost per row returned
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prorows `float4`

   Estimated number of result rows (zero if not proretset)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   provariadic `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type of the variadic array parameter\'s elements, or zero if the function does not have a variadic parameter
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prosupport `regproc` (references [pg_proc](#catalog-pg-proc).oid)

   Planner support function for this function (see [Function Optimization Information](braised:ref/xfunc-optimization)), or zero if none
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prokind `char`

   `f` for a normal function, `p` for a procedure, `a` for an aggregate function, or `w` for a window function
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prosecdef `bool`

   Function is a security definer (i.e., a "setuid" function)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proleakproof `bool`

   The function has no side effects. No information about the arguments is conveyed except via the return value. Any function that might throw an error depending on the values of its arguments is not leakproof.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proisstrict `bool`

   Function returns null if any call argument is null. In that case the function won\'t actually be called at all. Functions that are not "strict" must be prepared to handle null inputs.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proretset `bool`

   Function returns a set (i.e., multiple values of the specified data type)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   provolatile `char`

   provolatile tells whether the function\'s result depends only on its input arguments, or is affected by outside factors. It is `i` for "immutable" functions, which always deliver the same result for the same inputs. It is `s` for "stable" functions, whose results (for fixed inputs) do not change within a scan. It is `v` for "volatile" functions, whose results might change at any time. (Use `v` also for functions with side-effects, so that calls to them cannot get optimized away.)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proparallel `char`

   proparallel tells whether the function can be safely run in parallel mode. It is `s` for functions which are safe to run in parallel mode without restriction. It is `r` for functions which can be run in parallel mode, but their execution is restricted to the parallel group leader; parallel worker processes cannot invoke these functions. It is `u` for functions which are unsafe in parallel mode; the presence of such a function forces a serial execution plan.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pronargs `int2`

   Number of input arguments
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   pronargdefaults `int2`

   Number of arguments that have defaults
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prorettype `oid` (references [pg_type](#catalog-pg-type).oid)

   Data type of the return value
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proargtypes `oidvector` (references [pg_type](#catalog-pg-type).oid)

   An array of the data types of the function arguments. This includes only input arguments (including `INOUT` and `VARIADIC` arguments), and thus represents the call signature of the function.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proallargtypes `oid[]` (references [pg_type](#catalog-pg-type).oid)

   An array of the data types of the function arguments. This includes all arguments (including `OUT` and `INOUT` arguments); however, if all the arguments are `IN` arguments, this field will be null. Note that subscripting is 1-based, whereas for historical reasons proargtypes is subscripted from 0.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proargmodes `char[]`

   An array of the modes of the function arguments, encoded as `i` for `IN` arguments, `o` for `OUT` arguments, `b` for `INOUT` arguments, `v` for `VARIADIC` arguments, `t` for `TABLE` arguments. If all the arguments are `IN` arguments, this field will be null. Note that subscripts correspond to positions of proallargtypes not proargtypes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proargnames `text[]`

   An array of the names of the function arguments. Arguments without a name are set to empty strings in the array. If none of the arguments have a name, this field will be null. Note that subscripts correspond to positions of proallargtypes not proargtypes.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proargdefaults `pg_node_tree`

   Expression trees (in `nodeToString()` representation) for default values. This is a list with pronargdefaults elements, corresponding to the last *N* *input* arguments (i.e., the last *N* proargtypes positions). If none of the arguments have defaults, this field will be null.                                                                                                                                                                                                             |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   protrftypes `oid[]` (references [pg_type](#catalog-pg-type).oid)

   An array of the argument/result data type(s) for which to apply transforms (from the function\'s `TRANSFORM` clause). Null if none.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prosrc `text`

   This tells the function handler how to invoke the function. It might be the actual source code of the function for interpreted languages, a link symbol, a file name, or just about anything else, depending on the implementation language/call convention.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   probin `text`

   Additional information about how to invoke the function. Again, the interpretation is language-specific.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   prosqlbody `pg_node_tree`

   Pre-parsed SQL function body. This is used for SQL-language functions when the body is given in SQL-standard notation rather than as a string literal. It\'s null in other cases.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proconfig `text[]`

   Function\'s local settings for run-time configuration variables
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   proacl `aclitem[]`

   Access privileges; see [Privileges](braised:ref/ddl-priv) for details
  :::{/cell}
  :::{/row}
:::{/table}

: pg_proc Columns

For compiled functions, both built-in and dynamically loaded, prosrc contains the function\'s C-language name (link symbol). For SQL-language functions, prosrc contains the function\'s source text if that is specified as a string literal; but if the function body is specified in SQL-standard style, prosrc is unused (typically it\'s an empty string) and prosqlbody contains the pre-parsed definition. For all other currently-known language types, prosrc contains the function\'s source text. probin is null except for dynamically-loaded C functions, for which it gives the name of the shared library file containing the function.
