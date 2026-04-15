---
title: What Is PostgreSQL?
id: intro-whatis
hide_aside: true
---

PostgreSQL is an object-relational database management system (ORDBMS) based on [POSTGRES, Version 4.2](https://dsf.berkeley.edu/postgres.html), developed at the University of California at Berkeley Computer Science Department.
POSTGRES pioneered many concepts that only became available in some commercial database systems much later.

PostgreSQL is an open-source descendant of this original Berkeley code.
It supports a large part of the SQL standard and offers many modern features:

-   [complex queries](braised:ref/sql)
-   [foreign keys](braised:ref/ddl-constraints)
-   [triggers](braised:ref/triggers)
-   [updatable views](braised:ref/sql-createview)
-   [transactional integrity](braised:ref/transaction-iso)
-   [multiversion concurrency control](braised:ref/mvcc)

Also, PostgreSQL can be extended by the user in many ways, for example by adding new

-   [data types](braised:ref/datatype)
-   [functions](braised:ref/functions)
-   [operators](braised:ref/functions)
-   [aggregate functions](braised:ref/functions-aggregate)
-   [index methods](braised:ref/indexes)
-   [procedural languages](braised:ref/server-programming)

And because of the liberal license, PostgreSQL can be used, modified, and distributed by anyone free of charge for any purpose, be it private, commercial, or academic.
