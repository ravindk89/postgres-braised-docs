---
title: 40. Procedural Languages
id: xplang
---

PostgreSQL allows user-defined functions to be written in other languages besides SQL and C. These other languages are generically called procedural languages (PLs).
For a function written in a procedural language, the database server has no built-in knowledge about how to interpret the function\'s source text.
Instead, the task is passed to a special handler that knows the details of the language.
The handler could either do all the work of parsing, syntax analysis, execution, etc. itself, or it could serve as "glue" between PostgreSQL and an existing implementation of a programming language.
The handler itself is a C language function compiled into a shared object and loaded on demand, just like any other C function.

There are currently four procedural languages available in the standard PostgreSQL distribution: PL/pgSQL ([41. PL/pgSQL — SQL Procedural Language](braised:ref/plpgsql)), PL/Tcl ([42.
PL/Tcl — Tcl Procedural Language](braised:ref/pltcl)), PL/Perl ([43. PL/Perl — Perl Procedural Language](braised:ref/plperl)), and PL/Python ([44.
PL/Python — Python Procedural Language](braised:ref/plpython)).
There are additional procedural languages available that are not included in the core distribution. [H. External Projects](braised:ref/external-projects) has information about finding them.
In addition other languages can be defined by users; the basics of developing a new procedural language are covered in [57. Writing a Procedural Language Handler](braised:ref/plhandler).
