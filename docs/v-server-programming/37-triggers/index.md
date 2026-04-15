---
title: 37. Triggers
id: triggers
---

This chapter provides general information about writing trigger functions.
Trigger functions can be written in most of the available procedural languages, including PL/pgSQL ([41. PL/pgSQL — SQL Procedural Language](braised:ref/plpgsql)), PL/Tcl ([42.
PL/Tcl — Tcl Procedural Language](braised:ref/pltcl)), PL/Perl ([43. PL/Perl — Perl Procedural Language](braised:ref/plperl)), and PL/Python ([44.
PL/Python — Python Procedural Language](braised:ref/plpython)).
After reading this chapter, you should consult the chapter for your favorite procedural language to find out the language-specific details of writing a trigger in it.

It is also possible to write a trigger function in C, although most people find it easier to use one of the procedural languages.
It is not currently possible to write a trigger function in the plain SQL function language.
