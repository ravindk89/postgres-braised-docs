---
title: "44.4. Anonymous Code Blocks"
id: plpython-do
---

## Anonymous Code Blocks

PL/Python also supports anonymous code blocks called with the [DO](braised:ref/sql-do) statement:

    DO $$
        # PL/Python code
    $$ LANGUAGE plpython3u;

An anonymous code block receives no arguments, and whatever value it might return is discarded.
Otherwise it behaves just like a function.
