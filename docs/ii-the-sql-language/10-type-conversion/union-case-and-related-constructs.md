---
title: "10.5. UNION, CASE, and Related Constructs"
id: typeconv-union-case
---

## `UNION`, `CASE`, and Related Constructs

SQL `UNION` constructs must match up possibly dissimilar types to become a single result set.
The resolution algorithm is applied separately to each output column of a union query.
The `INTERSECT` and `EXCEPT` constructs resolve dissimilar types in the same way as `UNION`.
Some other constructs, including `CASE`, `ARRAY`, `VALUES`, and the `GREATEST` and `LEAST` functions, use the identical algorithm to match up their component expressions and select a result data type.

-   If all inputs are of the same type, and it is not `unknown`, resolve as that type.

-   If any input is of a domain type, treat it as being of the domain\'s base type for all subsequent steps. [^1]

-   If all inputs are of type `unknown`, resolve as type `text` (the preferred type of the string category). Otherwise, `unknown` inputs are ignored for the purposes of the remaining rules.

-   If the non-unknown inputs are not all of the same type category, fail.

-   Select the first non-unknown input type as the candidate type, then consider each other non-unknown input type, left to right. [^2] If the candidate type can be implicitly converted to the other type, but not vice-versa, select the other type as the new candidate type. Then continue considering the remaining inputs. If, at any stage of this process, a preferred type is selected, stop considering additional inputs.

-   Convert all inputs to the final candidate type. Fail if there is not an implicit conversion from a given input type to the candidate type.

Some examples follow.

    SELECT text 'a' AS "text" UNION SELECT 'b';

     text
    ------
     a
     b
    (2 rows)

Here, the unknown-type literal `'b'` will be resolved to type `text`.

    SELECT 1.2 AS "numeric" UNION SELECT 1;

     numeric
    ---------
           1
         1.2
    (2 rows)

The literal `1.2` is of type `numeric`, and the `integer` value `1` can be cast implicitly to `numeric`, so that type is used.

    SELECT 1 AS "real" UNION SELECT CAST('2.2' AS REAL);

     real
    ------
        1
      2.2
    (2 rows)

Here, since type `real` cannot be implicitly cast to `integer`, but `integer` can be implicitly cast to `real`, the union result type is resolved as `real`.

    SELECT NULL UNION SELECT NULL UNION SELECT 1;

    ERROR:  UNION types text and integer cannot be matched

This failure occurs because PostgreSQL treats multiple `UNION`s as a nest of pairwise operations; that is, this input is the same as

    (SELECT NULL UNION SELECT NULL) UNION SELECT 1;

The inner `UNION` is resolved as emitting type `text`, according to the rules given above.
Then the outer `UNION` has inputs of types `text` and `integer`, leading to the observed error.
The problem can be fixed by ensuring that the leftmost `UNION` has at least one input of the desired result type.

`INTERSECT` and `EXCEPT` operations are likewise resolved pairwise.
However, the other constructs described in this section consider all of their inputs in one resolution step.

[^1]: Somewhat like the treatment of domain inputs for operators and functions, this behavior allows a domain type to be preserved through a `UNION` or similar construct, so long as the user is careful to ensure that all inputs are implicitly or explicitly of that exact type.
Otherwise the domain\'s base type will be used.

[^2]: For historical reasons, `CASE` treats its `ELSE` clause (if any) as the "first" input, with the `THEN` clauses(s) considered after that.
In all other cases, "left to right" means the order in which the expressions appear in the query text.
