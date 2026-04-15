---
title: "9.11. Geometric Functions and Operators"
id: functions-geometry
---

## Geometric Functions and Operators

The geometric types `point`, `box`, `lseg`, `line`, `path`, `polygon`, and `circle` have a large set of native support functions and operators, shown in Geometric Operators, Geometric Functions, and Geometric Type Conversion Functions.

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
   *geometric_type* `+` `point` *geometric_type*                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

   Adds the coordinates of the second `point` to those of each point of the first argument, thus performing translation. Available for `point`, `box`, `path`, `circle`.

   `box '(1,1),(0,0)' + point '(2,0)'` (3,1),(2,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `path` `+` `path` path

   Concatenates two open paths (returns NULL if either path is closed).

   `path '[(0,0),(1,1)]' + path '[(2,2),(3,3),(4,4)]'` \[(0,0),(1,1),(2,2),(3,3),(4,4)\]
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `-` `point` *geometric_type*                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

   Subtracts the coordinates of the second `point` from those of each point of the first argument, thus performing translation. Available for `point`, `box`, `path`, `circle`.

   `box '(1,1),(0,0)' - point '(2,0)'` (-1,1),(-2,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `*` `point` *geometric_type*                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

   Multiplies each point of the first argument by the second `point` (treating a point as being a complex number represented by real and imaginary parts, and performing standard complex multiplication). If one interprets the second `point` as a vector, this is equivalent to scaling the object\'s size and distance from the origin by the length of the vector, and rotating it counterclockwise around the origin by the vector\'s angle from the *x* axis. Available for `point`, `box`,[^1] `path`, `circle`. |

   `path '((0,0),(1,0),(1,1))' * point '(3.0,0)'` ((0,0),(3,0),(3,3))

   `path '((0,0),(1,0),(1,1))' * point(cosd(45), sind(45))` ((0,0),​(0.7071067811865475,0.7071067811865475),​(0,1.414213562373095))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `/` `point` *geometric_type*                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

   Divides each point of the first argument by the second `point` (treating a point as being a complex number represented by real and imaginary parts, and performing standard complex division). If one interprets the second `point` as a vector, this is equivalent to scaling the object\'s size and distance from the origin down by the length of the vector, and rotating it clockwise around the origin by the vector\'s angle from the *x* axis. Available for `point`, `box`, `path`, `circle`.                |

   `path '((0,0),(1,0),(1,1))' / point '(2.0,0)'` ((0,0),(0.5,0),(0.5,0.5))

   `path '((0,0),(1,0),(1,1))' / point(cosd(45), sind(45))` ((0,0),​(0.7071067811865476,-0.7071067811865476),​(1.4142135623730951,0))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `@-@` *geometric_type* double precision                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

   Computes the total length. Available for `lseg`, `path`.

   `@-@ path '[(0,0),(1,0),(1,1)]'` 2
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `@@` *geometric_type* point                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

   Computes the center point. Available for `box`, `lseg`, `polygon`, `circle`.

   `@@ box '(2,2),(0,0)'` (1,1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `#` *geometric_type* integer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

   Returns the number of points. Available for `path`, `polygon`.

   `# path '((1,0),(0,1),(-1,0))'` 3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `#` *geometric_type* point                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

   Computes the point of intersection, or NULL if there is none. Available for `lseg`, `line`.

   `lseg '[(0,0),(1,1)]' # lseg '[(1,0),(0,1)]'` (0.5,0.5)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` `#` `box` box

   Computes the intersection of two boxes, or NULL if there is none.

   `box '(2,2),(-1,-1)' # box '(1,1),(-2,-2)'` (1,1),(-1,-1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `##` *geometric_type* point                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

   Computes the closest point to the first object on the second object. Available for these pairs of types: (`point`, `box`), (`point`, `lseg`), (`point`, `line`), (`lseg`, `box`), (`lseg`, `lseg`), (`line`, `lseg`).

   `point '(0,0)' ## lseg '[(2,0),(0,2)]'` (1,1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `<->` *geometric_type* double precision                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

   Computes the distance between the objects. Available for all seven geometric types, for all combinations of `point` with another geometric type, and for these additional pairs of types: (`box`, `lseg`), (`lseg`, `line`), (`polygon`, `circle`) (and the commutator cases).

   `circle '<(0,0),1>' <-> circle '<(5,0),1>'` 3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `@>` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Does first object contain second? Available for these pairs of types: (`box`, `point`), (`box`, `box`), (`path`, `point`), (`polygon`, `point`), (`polygon`, `polygon`), (`circle`, `point`), (`circle`, `circle`).

   `circle '<(0,0),2>' @> point '(1,1)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `<@` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Is first object contained in or on second? Available for these pairs of types: (`point`, `box`), (`point`, `lseg`), (`point`, `line`), (`point`, `path`), (`point`, `polygon`), (`point`, `circle`), (`box`, `box`), (`lseg`, `box`), (`lseg`, `line`), (`polygon`, `polygon`), (`circle`, `circle`).

   `point '(1,1)' <@ circle '<(0,0),2>'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `&&` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Do these objects overlap? (One point in common makes this true.) Available for `box`, `polygon`, `circle`.

   `box '(1,1),(0,0)' && box '(2,2),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `<<` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Is first object strictly left of second? Available for `point`, `box`, `polygon`, `circle`.

   `circle '<(0,0),1>' << circle '<(5,0),1>'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `>>` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Is first object strictly right of second? Available for `point`, `box`, `polygon`, `circle`.

   `circle '<(5,0),1>' >> circle '<(0,0),1>'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `&<` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Does first object not extend to the right of second? Available for `box`, `polygon`, `circle`.

   `box '(1,1),(0,0)' &< box '(2,2),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `&>` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Does first object not extend to the left of second? Available for `box`, `polygon`, `circle`.

   `box '(3,3),(0,0)' &> box '(2,2),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `<<|` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

   Is first object strictly below second? Available for `point`, `box`, `polygon`, `circle`.

   `box '(3,3),(0,0)' <<| box '(5,5),(3,4)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `|>>` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

   Is first object strictly above second? Available for `point`, `box`, `polygon`, `circle`.

   `box '(5,5),(3,4)' |>> box '(3,3),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `&<|` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

   Does first object not extend above second? Available for `box`, `polygon`, `circle`.

   `box '(1,1),(0,0)' &<| box '(2,2),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `|&>` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

   Does first object not extend below second? Available for `box`, `polygon`, `circle`.

   `box '(3,3),(0,0)' |&> box '(2,2),(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` `<^` `box` boolean

   Is first object below second (allows edges to touch)?

   `box '((1,1),(0,0))' <^ box '((2,2),(1,1))'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` `>^` `box` boolean

   Is first object above second (allows edges to touch)?

   `box '((2,2),(1,1))' >^ box '((1,1),(0,0))'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `?#` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Do these objects intersect? Available for these pairs of types: (`box`, `box`), (`lseg`, `box`), (`lseg`, `lseg`), (`lseg`, `line`), (`line`, `box`), (`line`, `line`), (`path`, `path`).

   `lseg '[(-1,0),(1,0)]' ?# box '(2,2),(-2,-2)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `?-` `line` boolean

   `?-` `lseg` boolean

   Is line horizontal?

   `?- lseg '[(-1,0),(1,0)]'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` `?-` `point` boolean

   Are points horizontally aligned (that is, have same y coordinate)?

   `point '(1,0)' ?- point '(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `?|` `line` boolean

   `?|` `lseg` boolean

   Is line vertical?

   `?| lseg '[(-1,0),(1,0)]'` f
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` `?|` `point` boolean

   Are points vertically aligned (that is, have same x coordinate)?

   `point '(0,1)' ?| point '(0,0)'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `line` `?-|` `line` boolean

   `lseg` `?-|` `lseg` boolean

   Are lines perpendicular?

   `lseg '[(0,0),(0,1)]' ?-| lseg '[(0,0),(1,0)]'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `line` `?||` `line` boolean

   `lseg` `?||` `lseg` boolean

   Are lines parallel?

   `lseg '[(-1,0),(1,0)]' ?|| lseg '[(-1,2),(1,2)]'` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   *geometric_type* `~=` *geometric_type* boolean                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

   Are these objects the same? Available for `point`, `box`, `polygon`, `circle`.

   `polygon '((0,0),(1,1))' ~= polygon '((1,1),(0,0))'` t
  :::{/cell}
  :::{/row}
:::{/table}

: Geometric Operators

:::{.callout type="caution"}
Note that the "same as" operator, `~=`, represents the usual notion of equality for the `point`, `box`, `polygon`, and `circle` types. Some of the geometric types also have an `=` operator, but `=` compares for equal *areas* only. The other scalar comparison operators (`<=` and so on), where available for these types, likewise compare areas.
:::

:::{.callout type="note"}
Before PostgreSQL 14, the point is strictly below/above comparison operators `point` `<<|` `point` and `point` `|>>` `point` were respectively called `<^` and `>^`. These names are still available, but are deprecated and will eventually be removed.
:::

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
   `area` ( *geometric_type* ) double precision                                                                                                                                       |

   Computes area. Available for `box`, `path`, `circle`. A `path` input must be closed, else NULL is returned. Also, if the `path` is self-intersecting, the result may be meaningless.

   `area(box '(2,2),(0,0)')` 4
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `center` ( *geometric_type* ) point                                                                                                                                                |

   Computes center point. Available for `box`, `circle`.

   `center(box '(1,2),(0,0)')` (0.5,1)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `diagonal` ( `box` ) lseg

   Extracts box\'s diagonal as a line segment (same as `lseg(box)`).

   `diagonal(box '(1,2),(0,0)')` \[(1,2),(0,0)\]
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `diameter` ( `circle` ) double precision

   Computes diameter of circle.

   `diameter(circle '<(0,0),2>')` 4
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `height` ( `box` ) double precision

   Computes vertical size of box.

   `height(box '(1,2),(0,0)')` 2
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `isclosed` ( `path` ) boolean

   Is path closed?

   `isclosed(path '((0,0),(1,1),(2,0))')` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `isopen` ( `path` ) boolean

   Is path open?

   `isopen(path '[(0,0),(1,1),(2,0)]')` t
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `length` ( *geometric_type* ) double precision                                                                                                                                     |

   Computes the total length. Available for `lseg`, `path`.

   `length(path '((-1,0),(1,0))')` 4
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `npoints` ( *geometric_type* ) integer                                                                                                                                             |

   Returns the number of points. Available for `path`, `polygon`.

   `npoints(path '[(0,0),(1,1),(2,0)]')` 3
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pclose` ( `path` ) path

   Converts path to closed form.

   `pclose(path '[(0,0),(1,1),(2,0)]')` ((0,0),(1,1),(2,0))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `popen` ( `path` ) path

   Converts path to open form.

   `popen(path '((0,0),(1,1),(2,0))')` \[(0,0),(1,1),(2,0)\]
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `radius` ( `circle` ) double precision

   Computes radius of circle.

   `radius(circle '<(0,0),2>')` 2
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `slope` ( `point`, `point` ) double precision

   Computes slope of a line drawn through the two points.

   `slope(point '(0,0)', point '(2,1)')` 0.5
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `width` ( `box` ) double precision

   Computes horizontal size of box.

   `width(box '(1,2),(0,0)')` 1
  :::{/cell}
  :::{/row}
:::{/table}

: Geometric Functions

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
   `box` ( `circle` ) box

   Computes box inscribed within the circle.

   `box(circle '<(0,0),2>')` (1.414213562373095,1.414213562373095),​(-1.414213562373095,-1.414213562373095)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` ( `point` ) box

   Converts point to empty box.

   `box(point '(1,0)')` (1,0),(1,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` ( `point`, `point` ) box

   Converts any two corner points to box.

   `box(point '(0,1)', point '(1,0)')` (1,1),(0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `box` ( `polygon` ) box

   Computes bounding box of polygon.

   `box(polygon '((0,0),(1,1),(2,0))')` (2,1),(0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `bound_box` ( `box`, `box` ) box

   Computes bounding box of two boxes.

   `bound_box(box '(1,1),(0,0)', box '(4,4),(3,3)')` (4,4),(0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `circle` ( `box` ) circle

   Computes smallest circle enclosing box.

   `circle(box '(1,1),(0,0)')` *(0.5,0.5),0.7071067811865476*                                                                                                                                                                                                                                                                                                                                                                                                   |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `circle` ( `point`, `double precision` ) circle

   Constructs circle from center and radius.

   `circle(point '(0,0)', 2.0)` *(0,0),2*                                                                                                                                                                                                                                                                                                                                                                                                                       |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `circle` ( `polygon` ) circle

   Converts polygon to circle. The circle\'s center is the mean of the positions of the polygon\'s points, and the radius is the average distance of the polygon\'s points from that center.

   `circle(polygon '((0,0),(1,3),(2,0))')` *(1,1),1.6094757082487299*                                                                                                                                                                                                                                                                                                                                                                                           |
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `line` ( `point`, `point` ) line

   Converts two points to the line through them.

   `line(point '(-1,0)', point '(1,0)')` {0,-1,0}
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lseg` ( `box` ) lseg

   Extracts box\'s diagonal as a line segment.

   `lseg(box '(1,0),(-1,0)')` \[(1,0),(-1,0)\]
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `lseg` ( `point`, `point` ) lseg

   Constructs line segment from two endpoints.

   `lseg(point '(-1,0)', point '(1,0)')` \[(-1,0),(1,0)\]
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `path` ( `polygon` ) path

   Converts polygon to a closed path with the same list of points.

   `path(polygon '((0,0),(1,1),(2,0))')` ((0,0),(1,1),(2,0))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` ( `double precision`, `double precision` ) point

   Constructs point from its coordinates.

   `point(23.4, -44.5)` (23.4,-44.5)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` ( `box` ) point

   Computes center of box.

   `point(box '(1,0),(-1,0)')` (0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` ( `circle` ) point

   Computes center of circle.

   `point(circle '<(0,0),2>')` (0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` ( `lseg` ) point

   Computes center of line segment.

   `point(lseg '[(-1,0),(1,0)]')` (0,0)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` ( `polygon` ) point

   Computes center of polygon (the mean of the positions of the polygon\'s points).

   `point(polygon '((0,0),(1,1),(2,0))')` (1,0.3333333333333333)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `polygon` ( `box` ) polygon

   Converts box to a 4-point polygon.

   `polygon(box '(1,1),(0,0)')` ((0,0),(0,1),(1,1),(1,0))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `polygon` ( `circle` ) polygon

   Converts circle to a 12-point polygon.

   `polygon(circle '<(0,0),2>')` ((-2,0),​(-1.7320508075688774,0.9999999999999999),​(-1.0000000000000002,1.7320508075688772),​(-1.2246063538223773e-16,2),​(0.9999999999999996,1.7320508075688774),​(1.732050807568877,1.0000000000000007),​(2,2.4492127076447545e-16),​(1.7320508075688776,-0.9999999999999994),​(1.0000000000000009,-1.7320508075688767),​(3.673819061467132e-16,-2),​(-0.9999999999999987,-1.732050807568878),​(-1.7320508075688767,-1.00000000
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `polygon` ( `integer`, `circle` ) polygon

   Converts circle to an *n*-point polygon.                                                                                                                                                                                                                                                                                                                                                                                                                     |

   `polygon(4, circle '<(3,0),1>')` ((2,0),​(3,1),​(4,1.2246063538223773e-16),​(3,-1))
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `polygon` ( `path` ) polygon

   Converts closed path to a polygon with the same list of points.

   `polygon(path '((0,0),(1,1),(2,0))')` ((0,0),(1,1),(2,0))
  :::{/cell}
  :::{/row}
:::{/table}

: Geometric Type Conversion Functions

It is possible to access the two component numbers of a `point` as though the point were an array with indexes 0 and 1. For example, if `t.p` is a `point` column then `SELECT p[0] FROM t` retrieves the X coordinate and `UPDATE t SET p[1] = ...` changes the Y coordinate. In the same way, a value of type `box` or `lseg` can be treated as an array of two `point` values.

[^1]: "Rotating" a box with these operators only moves its corner points: the box is still considered to have sides parallel to the axes. Hence the box\'s size is not preserved, as a true rotation would do.
