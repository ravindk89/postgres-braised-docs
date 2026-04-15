---
title: "44.5. Trigger Functions"
id: plpython-trigger
---

## Trigger Functions

When a function is used as a trigger, the dictionary `TD` contains trigger-related values:

:::{.dl}
:::{.item term="`TD['event']`"}
contains the event as a string: `INSERT`, `UPDATE`, `DELETE`, or `TRUNCATE`.
:::{/item}
:::{.item term="`TD['when']`"}
contains one of `BEFORE`, `AFTER`, or `INSTEAD OF`.
:::{/item}
:::{.item term="`TD['level']`"}
contains `ROW` or `STATEMENT`.
:::{/item}
:::{.item term="`TD['new']`; `TD['old']`"}
For a row-level trigger, one or both of these fields contain the respective trigger rows, depending on the trigger event.
:::{/item}
:::{.item term="`TD['name']`"}
contains the trigger name.
:::{/item}
:::{.item term="`TD['table_name']`"}
contains the name of the table on which the trigger occurred.
:::{/item}
:::{.item term="`TD['table_schema']`"}
contains the schema of the table on which the trigger occurred.
:::{/item}
:::{.item term="`TD['relid']`"}
contains the OID of the table on which the trigger occurred.
:::{/item}
:::{.item term="`TD['args']`"}
If the `CREATE TRIGGER` command included arguments, they are available in `TD["args"][0]` to `TD["args"][n-1]`.
:::{/item}
:::{/dl}

If `TD["when"]` is `BEFORE` or `INSTEAD OF` and `TD["level"]` is `ROW`, you can return `None` or `"OK"` from the Python function to indicate the row is unmodified, `"SKIP"` to abort the event, or if `TD["event"]` is `INSERT` or `UPDATE` you can return `"MODIFY"` to indicate you\'ve modified the new row.
Otherwise the return value is ignored.
