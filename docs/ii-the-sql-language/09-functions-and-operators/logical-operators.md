---
title: "9.1. Logical Operators"
id: functions-logical
---

## Logical Operators

The usual logical operators are available: `boolean` `AND` `boolean` boolean `boolean` `OR` `boolean` boolean `NOT` `boolean` boolean SQL uses a three-valued logic system with true, false, and `null`, which represents "unknown".
Observe the following truth tables:

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  *a*   *
  :::{/cell}
  :::{.cell}
  *   *a*
  :::{/cell}
  :::{.cell}
  AND *b*   *a* OR
  :::{/cell}
  :::{.cell}
  b*
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{/row}
:::{/table}

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  *a*   N
  :::{/cell}
  :::{.cell}
  T *a*
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  FALSE
  :::{/cell}
  :::{.cell}
  TRUE
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  NULL
  :::{/cell}
  :::{.cell}
  NULL
  :::{/cell}
  :::{/row}
:::{/table}

The operators `AND` and `OR` are commutative, that is, you can switch the left and right operands without affecting the result. (However, it is not guaranteed that the left operand is evaluated before the right operand. See [Expression Evaluation Rules](braised:ref/sql-expressions#expression-evaluation-rules) for more information about the order of evaluation of subexpressions.)
