---
title: "9.20. Range/Multirange Functions and Operators"
id: functions-range
---

## Range/Multirange Functions and Operators

See [Range Types](braised:ref/rangetypes) for an overview of range types.

Range Operators shows the specialized operators available for range types. Multirange Operators shows the specialized operators available for multirange types.
In addition to those, the usual comparison operators shown in [Comparison Operators](braised:ref/functions-comparison#comparison-operators) are available for range and multirange types.
The comparison operators order first by the range lower bounds, and only if those are equal do they compare the upper bounds.
The multirange operators compare each range until one is unequal.
This does not usually result in a useful overall ordering, but the operators are provided to allow unique indexes to be constructed on ranges.

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
   `anyrange` `@>` `anyrange` boolean

   Does the first range contain the second?

   `int4range(2,4) @> int4range(2,3)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `@>` `anyelement` boolean

   Does the range contain the element?

   `'[2011-01-01,2011-03-01)'::tsrange @> '2011-01-10'::timestamp` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `<@` `anyrange` boolean

   Is the first range contained by the second?

   `int4range(2,4) <@ int4range(1,7)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyelement` `<@` `anyrange` boolean

   Is the element contained in the range?

   `42 <@ int4range(1,7)` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&&` `anyrange` boolean

   Do the ranges overlap, that is, have any elements in common?

   `int8range(3,7) && int8range(4,12)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `<<` `anyrange` boolean

   Is the first range strictly left of the second?

   `int8range(1,10) << int8range(100,110)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `>>` `anyrange` boolean

   Is the first range strictly right of the second?

   `int8range(50,60) >> int8range(20,30)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&<` `anyrange` boolean

   Does the first range not extend to the right of the second?

   `int8range(1,20) &< int8range(18,20)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&>` `anyrange` boolean

   Does the first range not extend to the left of the second?

   `int8range(7,20) &> int8range(5,10)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `-|-` `anyrange` boolean

   Are the ranges adjacent?

   `numrange(1.1,2.2) -|- numrange(2.2,3.3)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `+` `anyrange` anyrange

   Computes the union of the ranges. The ranges must overlap or be adjacent, so that the union is a single range (but see `range_merge()`).

   `numrange(5,15) + numrange(10,20)` \[5,20)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `*` `anyrange` anyrange

   Computes the intersection of the ranges.

   `int8range(5,15) * int8range(10,20)` \[10,15)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `-` `anyrange` anyrange

   Computes the difference of the ranges. The second range must not be contained in the first in such a way that the difference would not be a single range.

   `int8range(5,15) - int8range(10,20)` \[5,10)
  :::{/cell}
  :::{/row}
:::{/table}

: Range Operators

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
   `anymultirange` `@>` `anymultirange` boolean

   Does the first multirange contain the second?

   `'{[2,4)}'::int4multirange @> '{[2,3)}'::int4multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `@>` `anyrange` boolean

   Does the multirange contain the range?

   `'{[2,4)}'::int4multirange @> int4range(2,3)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `@>` `anyelement` boolean

   Does the multirange contain the element?

   `'{[2011-01-01,2011-03-01)}'::tsmultirange @> '2011-01-10'::timestamp` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `@>` `anymultirange` boolean

   Does the range contain the multirange?

   `'[2,4)'::int4range @> '{[2,3)}'::int4multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `<@` `anymultirange` boolean

   Is the first multirange contained by the second?

   `'{[2,4)}'::int4multirange <@ '{[1,7)}'::int4multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `<@` `anyrange` boolean

   Is the multirange contained by the range?

   `'{[2,4)}'::int4multirange <@ int4range(1,7)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `<@` `anymultirange` boolean

   Is the range contained by the multirange?

   `int4range(2,4) <@ '{[1,7)}'::int4multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyelement` `<@` `anymultirange` boolean

   Is the element contained by the multirange?

   `4 <@ '{[1,7)}'::int4multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&&` `anymultirange` boolean

   Do the multiranges overlap, that is, have any elements in common?

   `'{[3,7)}'::int8multirange && '{[4,12)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&&` `anyrange` boolean

   Does the multirange overlap the range?

   `'{[3,7)}'::int8multirange && int8range(4,12)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&&` `anymultirange` boolean

   Does the range overlap the multirange?

   `int8range(3,7) && '{[4,12)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `<<` `anymultirange` boolean

   Is the first multirange strictly left of the second?

   `'{[1,10)}'::int8multirange << '{[100,110)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `<<` `anyrange` boolean

   Is the multirange strictly left of the range?

   `'{[1,10)}'::int8multirange << int8range(100,110)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `<<` `anymultirange` boolean

   Is the range strictly left of the multirange?

   `int8range(1,10) << '{[100,110)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `>>` `anymultirange` boolean

   Is the first multirange strictly right of the second?

   `'{[50,60)}'::int8multirange >> '{[20,30)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `>>` `anyrange` boolean

   Is the multirange strictly right of the range?

   `'{[50,60)}'::int8multirange >> int8range(20,30)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `>>` `anymultirange` boolean

   Is the range strictly right of the multirange?

   `int8range(50,60) >> '{[20,30)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&<` `anymultirange` boolean

   Does the first multirange not extend to the right of the second?

   `'{[1,20)}'::int8multirange &< '{[18,20)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&<` `anyrange` boolean

   Does the multirange not extend to the right of the range?

   `'{[1,20)}'::int8multirange &< int8range(18,20)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&<` `anymultirange` boolean

   Does the range not extend to the right of the multirange?

   `int8range(1,20) &< '{[18,20)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&>` `anymultirange` boolean

   Does the first multirange not extend to the left of the second?

   `'{[7,20)}'::int8multirange &> '{[5,10)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `&>` `anyrange` boolean

   Does the multirange not extend to the left of the range?

   `'{[7,20)}'::int8multirange &> int8range(5,10)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `&>` `anymultirange` boolean

   Does the range not extend to the left of the multirange?

   `int8range(7,20) &> '{[5,10)}'::int8multirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `-|-` `anymultirange` boolean

   Are the multiranges adjacent?

   `'{[1.1,2.2)}'::nummultirange -|- '{[2.2,3.3)}'::nummultirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `-|-` `anyrange` boolean

   Is the multirange adjacent to the range?

   `'{[1.1,2.2)}'::nummultirange -|- numrange(2.2,3.3)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anyrange` `-|-` `anymultirange` boolean

   Is the range adjacent to the multirange?

   `numrange(1.1,2.2) -|- '{[2.2,3.3)}'::nummultirange` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `+` `anymultirange` anymultirange

   Computes the union of the multiranges. The multiranges need not overlap or be adjacent.

   `'{[5,10)}'::nummultirange + '{[15,20)}'::nummultirange` {\[5,10), \[15,20)}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `*` `anymultirange` anymultirange

   Computes the intersection of the multiranges.

   `'{[5,15)}'::int8multirange * '{[10,20)}'::int8multirange` {\[10,15)}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `anymultirange` `-` `anymultirange` anymultirange

   Computes the difference of the multiranges.

   `'{[5,20)}'::int8multirange - '{[10,15)}'::int8multirange` {\[5,10), \[15,20)}
  :::{/cell}
  :::{/row}
:::{/table}

: Multirange Operators

The left-of/right-of/adjacent operators always return false when an empty range or multirange is involved; that is, an empty range is not considered to be either before or after any other range.

Elsewhere empty ranges and multiranges are treated as the additive identity: anything unioned with an empty value is itself. Anything minus an empty value is itself. An empty multirange has exactly the same points as an empty range. Every range contains the empty range. Every multirange contains as many empty ranges as you like.

The range union and difference operators will fail if the resulting range would need to contain two disjoint sub-ranges, as such a range cannot be represented. There are separate operators for union and difference that take multirange parameters and return a multirange, and they do not fail even if their arguments are disjoint. So if you need a union or difference operation for ranges that may be disjoint, you can avoid errors by first casting your ranges to multiranges.

Range Functions shows the functions available for use with range types. Multirange Functions shows the functions available for use with multirange types.

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
   `lower` ( `anyrange` ) anyelement

   Extracts the lower bound of the range (`NULL` if the range is empty or has no lower bound).

   `lower(numrange(1.1,2.2))` 1.1
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper` ( `anyrange` ) anyelement

   Extracts the upper bound of the range (`NULL` if the range is empty or has no upper bound).

   `upper(numrange(1.1,2.2))` 2.2
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `isempty` ( `anyrange` ) boolean

   Is the range empty?

   `isempty(numrange(1.1,2.2))` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lower_inc` ( `anyrange` ) boolean

   Is the range\'s lower bound inclusive?

   `lower_inc(numrange(1.1,2.2))` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper_inc` ( `anyrange` ) boolean

   Is the range\'s upper bound inclusive?

   `upper_inc(numrange(1.1,2.2))` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lower_inf` ( `anyrange` ) boolean

   Does the range have no lower bound? (A lower bound of `-Infinity` returns false.)

   `lower_inf('(,)'::daterange)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper_inf` ( `anyrange` ) boolean

   Does the range have no upper bound? (An upper bound of `Infinity` returns false.)

   `upper_inf('(,)'::daterange)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `range_merge` ( `anyrange`, `anyrange` ) anyrange

   Computes the smallest range that includes both of the given ranges.

   `range_merge('[1,2)'::int4range, '[3,4)'::int4range)` \[1,4)
  :::{/cell}
  :::{/row}
:::{/table}

: Range Functions

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
   `lower` ( `anymultirange` ) anyelement

   Extracts the lower bound of the multirange (`NULL` if the multirange is empty or has no lower bound).

   `lower('{[1.1,2.2)}'::nummultirange)` 1.1
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper` ( `anymultirange` ) anyelement

   Extracts the upper bound of the multirange (`NULL` if the multirange is empty or has no upper bound).

   `upper('{[1.1,2.2)}'::nummultirange)` 2.2
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `isempty` ( `anymultirange` ) boolean

   Is the multirange empty?

   `isempty('{[1.1,2.2)}'::nummultirange)` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lower_inc` ( `anymultirange` ) boolean

   Is the multirange\'s lower bound inclusive?

   `lower_inc('{[1.1,2.2)}'::nummultirange)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper_inc` ( `anymultirange` ) boolean

   Is the multirange\'s upper bound inclusive?

   `upper_inc('{[1.1,2.2)}'::nummultirange)` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lower_inf` ( `anymultirange` ) boolean

   Does the multirange have no lower bound? (A lower bound of `-Infinity` returns false.)

   `lower_inf('{(,)}'::datemultirange)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `upper_inf` ( `anymultirange` ) boolean

   Does the multirange have no upper bound? (An upper bound of `Infinity` returns false.)

   `upper_inf('{(,)}'::datemultirange)` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `range_merge` ( `anymultirange` ) anyrange

   Computes the smallest range that includes the entire multirange.

   `range_merge('{[1,2), [3,4)}'::int4multirange)` \[1,4)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `multirange` ( `anyrange` ) anymultirange

   Returns a multirange containing just the given range.

   `multirange('[1,2)'::int4range)` {\[1,2)}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `unnest` ( `anymultirange` ) setof anyrange

   Expands a multirange into a set of ranges in ascending order.

   `unnest('{[1,2), [3,4)}'::int4multirange)`

        [1,2)
        [3,4)
  :::{/cell}
  :::{/row}
:::{/table}

: Multirange Functions

The `lower_inc`, `upper_inc`, `lower_inf`, and `upper_inf` functions all return false for an empty range or multirange.
