---
title: 32. libpq — C Library
id: libpq
---

libpq is the C application programmer\'s interface to PostgreSQL. libpq is a set of library functions that allow client programs to pass queries to the PostgreSQL backend server and to receive the results of these queries.

libpq is also the underlying engine for several other PostgreSQL application interfaces, including those written for C++, Perl, Python, Tcl and ECPG.
So some aspects of libpq\'s behavior will be important to you if you use one of those packages.
In particular, [Section 32.15](braised:ref/libpq-envars), [Section 32.16](braised:ref/libpq-pgpass) and [Section 32.19](braised:ref/libpq-ssl) describe behavior that is visible to the user of any application that uses libpq.

Some short programs are included at the end of this chapter ([Section 32.23](braised:ref/libpq-example)) to show how to write programs that use libpq.
There are also several complete examples of libpq applications in the directory `src/test/examples` in the source code distribution.

Client programs that use libpq must include the header file `libpq-fe.h`libpq library.
