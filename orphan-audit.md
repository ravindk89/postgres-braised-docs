# Orphan Audit Report

**Total orphans classified:** 770  
**Generated from:** `orphans.tsv` (770 entries)

## Summary

| Category | Count | Description |
|---|---|---|
| FIXED | 168 | Intro sentence confirmed present in file — script applied correctly |
| WOULD_FIX | 15 | Script logic matches but intro not yet in file — check manually |
| FALSE_POS | 134 | refpurpose / synopsis / screen — not a dropped prose sentence |
| NO_XML_MATCH | 241 | First 55 chars not found in XML — encoding/inline-tag mismatch |
| AMBIGUOUS | 40 | Multiple XML para hits, couldn't disambiguate |
| ALREADY | 31 | Duplicate insert point — sibling orphan already handled this para |
| OTHER | 141 | Trivial intro, bad insert point, or file missing |

## FIXED (168)

_Script applied correctly — intro is present in file_

### `i-tutorial/the-sql-language/aggregate-functions.md`

- **line 24:** `but this will not work since the aggregate `max` cannot be used in the `WHERE` c`
  - _intro at line ~24: If we wanted to know what city (or cities) that reading occurred in, we might tr_
- **line 63:** `which gives us the same results for only the cities that have all temp_lo values`
  - _intro at line ~43: Aggregates are also very useful in combination with `GROUP BY` clauses. For exam_

### `i-tutorial/the-sql-language/populating-a-table-with-rows.md`

- **line 42:** `where the file name for the source file must be available on the machine running`
  - _intro at line ~42: You could also have used `COPY` to load large amounts of data from flat-text fil_

### `ii-the-sql-language/04-sql-syntax/lexical-structure.md`

- **line 52:** `can equivalently be written as:`
  - _intro at line ~20: Key words and unquoted identifiers are case-insensitive. Therefore:_
- **line 126:** `is not valid syntax. (This slightly bizarre behavior is specified by SQL; Postgr`
  - _intro at line ~116: Two string constants that are only separated by whitespace _with at least one ne_

### `ii-the-sql-language/05-data-definition/default-values.md`

- **line 31:** `where the `nextval()` function supplies successive values from a sequence object`
  - _intro at line ~17: The default value can be an expression, which will be evaluated whenever the def_

### `ii-the-sql-language/05-data-definition/dependency-tracking.md`

- **line 24:** `and all the dependent objects will be removed, as will any objects that depend o`
  - _intro at line ~14: To ensure the integrity of the entire database structure, PostgreSQL makes sure _

### `ii-the-sql-language/05-data-definition/identity-columns.md`

- **line 19:** `or alternatively`
  - _intro at line ~14: To create an identity column, use the `GENERATED ... AS IDENTITY` clause in `CRE_
- **line 34:** `would generate values for the `id` column starting at 1 and result in the follow`
  - _intro at line ~31: If an `INSERT` command is executed on the table with the identity column and no _

### `ii-the-sql-language/05-data-definition/inheritance.md`

- **line 91:** `which returns:`
  - _intro at line ~73: In some cases you might wish to know which table a particular row originated fro_

### `ii-the-sql-language/05-data-definition/row-security-policies.md`

- **line 277:** `and her transaction is in `READ COMMITTED` mode, it is possible for her to see "`
  - _intro at line ~275: That looks safe; there is no window wherein `mallory` should be able to see the _

### `ii-the-sql-language/06-data-manipulation/deleting-data.md`

- **line 25:** `then all rows in the table will be deleted!`
  - _intro at line ~23: If you simply write:_

### `ii-the-sql-language/07-queries/select-lists.md`

- **line 52:** `but either of these do:`
  - _intro at line ~50: The `AS` key word is usually optional, but in some cases where the desired colum_

### `ii-the-sql-language/07-queries/sorting-rows-order-by.md`

- **line 34:** `both of which sort by the first output column.`
  - _intro at line ~31: A _sort_expression_ can also be the column label or number of an output column, _

### `ii-the-sql-language/07-queries/table-expressions.md`

- **line 261:** `is not valid; the table alias `a` is not visible outside the alias `c`.`
  - _intro at line ~257: When an alias is applied to the output of a `JOIN` clause, the alias hides the o_
- **line 507:** `or in several other equivalent formulations. (As already mentioned, the `LATERAL`
  - _intro at line ~486: A trivial example of `LATERAL` is_
- **line 533:** `or perhaps even:`
  - _intro at line ~529: The join condition of an inner join can be written either in the `WHERE` clause _
- **line 714:** `represents the given list of expressions and all prefixes of the list including `
  - _intro at line ~714: A shorthand notation is provided for specifying two common types of grouping set_
- **line 730:** `represents the given list and all of its possible subsets (i.e., the power set).`
  - _intro at line ~730: A clause of the form_

### `ii-the-sql-language/07-queries/with-queries-common-table-expressions.md`

- **line 34:** `which displays per-product sales totals in only the top sales regions.`
  - _intro at line ~17: The basic value of `SELECT` in `WITH` is to break down complicated queries into _
- **line 250:** `and it will be internally rewritten to the above form.`
  - _intro at line ~187: There is built-in syntax to simplify cycle detection. The above query can also b_
- **line 305:** `the `WITH` query will be materialized, producing a temporary copy of big_table t`
  - _intro at line ~289: A simple example of these rules is_
- **line 403:** `the outer `SELECT` would return the updated data.`
  - _intro at line ~361: The sub-statements in `WITH` are executed concurrently with each other and with _

### `ii-the-sql-language/08-data-types/arrays.md`

- **line 237:** `or updated in a slice:`
  - _intro at line ~224: An array value can be replaced completely:_

### `ii-the-sql-language/08-data-types/composite-types.md`

- **line 39:** `or functions:`
  - _intro at line ~32: Having defined the types, we can use them to create tables:_
- **line 55:** `then the same `inventory_item` composite type shown above would come into being `
  - _intro at line ~49: Whenever you create a table, a composite type is also automatically created, wit_
- **line 65:** `which would be a valid value of the `inventory_item` type defined above.`
  - _intro at line ~63: To write a composite value as a literal constant, enclose the field values withi_
- **line 108:** `or if you need to use the table name as well (for instance in a multitable query`
  - _intro at line ~101: To access a field of a composite column, one writes a dot and the field name, mu_
- **line 178:** `as if the query were`
  - _intro at line ~169: When we write_
- **line 251:** `the whitespace will be ignored if the field type is integer, but not if it is te`
  - _intro at line ~249: The external text representation of a composite value consists of items that are_

### `ii-the-sql-language/08-data-types/date-time-types.md`

- **line 416:** `is supported.`
  - _intro at line ~406: Valid input for the time stamp types consists of the concatenation of a date and_

### `ii-the-sql-language/08-data-types/json-types.md`

- **line 208:** `but that approach is less flexible, and often less efficient as well.`
  - _intro at line ~206: Because JSON containment is nested, an appropriate query can skip explicit selec_

### `ii-the-sql-language/08-data-types/numeric-types.md`

- **line 87:** `selects a scale of 0. Specifying:`
  - _intro at line ~85: Both the maximum precision and the maximum scale of a `numeric` column can be co_
- **line 103:** `will round values to 1 decimal place and can store values between -99.9 and 99.9`
  - _intro at line ~101: If the scale of a value to be stored is greater than the declared scale of the c_
- **line 119:** `will round values to 5 decimal places and can store values between -0.00999 and `
  - _intro at line ~110: Beginning in PostgreSQL 15, it is allowed to declare a `numeric` column with a n_

### `ii-the-sql-language/08-data-types/object-identifier-types.md`

- **line 25:** `rather than:`
  - _intro at line ~23: The OID alias types have no operations of their own except for specialized input_

### `ii-the-sql-language/09-functions-and-operators/aggregate-functions.md`

- **line 395:** `will require effort proportional to the size of the table: PostgreSQL will need `
  - _intro at line ~393: Users accustomed to working with other SQL database management systems might be _

### `ii-the-sql-language/09-functions-and-operators/xml-functions.md`

- **line 915:** `where `xsi` is the XML namespace prefix for XML Schema Instance.`
  - _intro at line ~913: The parameter `nulls` determines whether null values should be included in the o_
- **line 945:** `where the format of a table mapping depends on the `tableforest` parameter as ex`
  - _intro at line ~943: The result of a schema content mapping looks like this:_
- **line 963:** `where the schema mapping is as above.`
  - _intro at line ~961: The result of a database content mapping looks like this:_

### `ii-the-sql-language/10-type-conversion/operators.md`

- **line 146:** `so that the `mytext` `=` `text` operator is found immediately according to the e`
  - _intro at line ~133: Users sometimes try to declare operators applying just to a domain type. This is_

### `ii-the-sql-language/10-type-conversion/select-output-columns.md`

- **line 13:** `there is nothing to identify what type the string literal should be taken as.`
  - _intro at line ~11: The rules given in the preceding sections will result in assignment of non-`unkn_

### `ii-the-sql-language/11-indexes/index-only-scans-and-covering-indexes.md`

- **line 59:** `could handle these queries as index-only scans, because `y` can be obtained from`
  - _intro at line ~54: To make effective use of the index-only scan feature, you might choose to create_
- **line 79:** `even though they had no intention of ever using `y` as part of a `WHERE` clause.`
  - _intro at line ~79: Before PostgreSQL had the `INCLUDE` feature, people sometimes made covering inde_
- **line 94:** `as an index-only scan; and this is very attractive if `f()` is an expensive-to-c`
  - _intro at line ~94: In principle, index-only scans can be used with expression indexes. For example,_

### `ii-the-sql-language/11-indexes/indexes-and-collations.md`

- **line 31:** `are also of interest, an additional index could be created that supports the `"y`
  - _intro at line ~13: Consider these statements:_

### `ii-the-sql-language/11-indexes/indexes-on-expressions.md`

- **line 26:** `then it might be worth creating an index like this:`
  - _intro at line ~24: As another example, if one often does queries like:_

### `ii-the-sql-language/11-indexes/introduction.md`

- **line 15:** `and the application issues many queries of the form:`
  - _intro at line ~10: Suppose we have a table similar to this:_

### `ii-the-sql-language/11-indexes/multicolumn-indexes.md`

- **line 21:** `then it might be appropriate to define an index on the columns major and minor t`
  - _intro at line ~11: An index can be defined on more than one column of a table. For example, if you _

### `ii-the-sql-language/12-full-text-search/introduction.md`

- **line 105:** `since here no normalization of the word `rats` will occur.`
  - _intro at line ~93: As the above example suggests, a `tsquery` is not just raw text, any more than a_

### `ii-the-sql-language/12-full-text-search/tables-and-indexes.md`

- **line 66:** `where `config_name` is a column in the `pgweb` table.`
  - _intro at line ~52: It is possible to set up more complex expression indexes wherein the configurati_

### `ii-the-sql-language/14-performance-tips/controlling-the-planner-with-explicit-join-clauses.md`

- **line 15:** `the planner is free to join the given tables in any order.`
  - _intro at line ~13: In a simple join query, such as:_
- **line 40:** `it is valid to join A to either B or C first.`
  - _intro at line ~31: When the query involves outer joins, the planner has less freedom than it does f_

### `ii-the-sql-language/14-performance-tips/statistics-used-by-the-planner.md`

- **line 155:** `even though there will really be zero rows satisfying this query.`
  - _intro at line ~148: When estimating with functional dependencies, the planner assumes that condition_

### `ii-the-sql-language/14-performance-tips/using-explain.md`

- **line 76:** `you will find that `tenk1` has 345 disk pages and 10000 rows.`
  - _intro at line ~74: These numbers are derived very straightforwardly. If you do:_
- **line 323:** `which shows that the planner thinks that hash join would be nearly 50% more expe`
  - _intro at line ~306: One way to look at variant plans is to force the planner to disregard whatever s_
- **line 697:** `the estimated cost and row count for the Index Scan node are shown as though it `
  - _intro at line ~480: There are cases in which the actual and estimated values won't match up well, bu_

### `iii-server-administration/17-installation-from-source-code/platform-specific-notes.md`

- **line 144:** `your DTrace installation is too old to handle probes in static functions.`
  - _intro at line ~136: If you see the linking of the `postgres` executable abort with an error message _

### `iii-server-administration/17-installation-from-source-code/post-installation-setup.md`

- **line 36:** `then this step was necessary.`
  - _intro at line ~33: If in doubt, refer to the manual pages of your system (perhaps `ld.so` or `rld`)_

### `iii-server-administration/18-server-setup-and-operation/managing-kernel-resources.md`

- **line 214:** `in `/etc/systemd/logind.conf` or another appropriate configuration file.`
  - _intro at line ~212: Alternatively, if the user account was created incorrectly or cannot be changed,_
- **line 301:** `in the PostgreSQL startup script just before invoking `postgres`.`
  - _intro at line ~299: Another approach, which can be used with or without altering `vm.overcommit_memo_

### `iii-server-administration/18-server-setup-and-operation/secure-tcp-ip-connections-with-ssh-tunnels.md`

- **line 34:** `but then the database server will see the connection as coming in on its `foo.co`
  - _intro at line ~32: You could also have set up port forwarding as_

### `iii-server-administration/18-server-setup-and-operation/secure-tcp-ip-connections-with-ssl.md`

- **line 180:** `because the server will reject the file if its permissions are more liberal than`
  - _intro at line ~173: To create a simple self-signed certificate for the server, valid for 365 days, u_

### `iii-server-administration/18-server-setup-and-operation/starting-the-database-server.md`

- **line 19:** `which will leave the server running in the foreground.`
  - _intro at line ~17: The bare-bones way to start the server manually is just to invoke `postgres` dir_
- **line 40:** `will start the server in the background and put the output into the named log fi`
  - _intro at line ~38: This shell syntax can get tedious quickly. Therefore the wrapper program is prov_

### `iii-server-administration/18-server-setup-and-operation/upgrading-a-postgresql-cluster.md`

- **line 107:** `to transfer your data.`
  - _intro at line ~105: The least downtime can be achieved by installing the new server in a different d_

### `iii-server-administration/20-client-authentication/user-name-maps.md`

- **line 43:** `will remove the domain part for users with system user names that end with `@myd`
  - _intro at line ~40: If the _system-username_ field starts with a slash (`/`), the remainder of the f_

### `iii-server-administration/21-database-roles/role-membership.md`

- **line 40:** `the session would have use of only those privileges granted to `wheel`, and not `
  - _intro at line ~21: The members of a group role can use the privileges of the role in two ways. Firs_

### `iii-server-administration/22-managing-databases/creating-a-database.md`

- **line 40:** `from the SQL environment, or:`
  - _intro at line ~38: Sometimes you want to create a database for someone else, and have them become t_

### `iii-server-administration/23-localization/character-set-support.md`

- **line 165:** `sets the default character set to `EUC_JP` (Extended Unix Code for Japanese). Yo`
  - _intro at line ~163: `initdb` defines the default character set (encoding) for a PostgreSQL cluster. _

### `iii-server-administration/23-localization/collation-support.md`

- **line 90:** `results in an error, because even though the `||` operator doesn\'t need to know`
  - _intro at line ~85: The collation assigned to a function or operator's combined input expressions is_
- **line 167:** `will draw an error even though the `C` and `POSIX` collations have identical beh`
  - _intro at line ~167: PostgreSQL considers distinct collation objects to be incompatible even when the_

### `iii-server-administration/24-routine-database-maintenance-tasks/routine-vacuuming.md`

- **line 345:** `is compared to the total number of tuples inserted, updated, or deleted since th`
  - _intro at line ~343: For analyze, a similar condition is used: the threshold, defined as:_

### `iii-server-administration/25-backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md`

- **line 295:** `which will copy previously archived WAL segments from the directory `/mnt/server`
  - _intro at line ~295: The key part of all this is to set up a recovery configuration that describes ho_

### `iii-server-administration/31-regression-tests/running-the-tests.md`

- **line 25:** `or otherwise a note about which tests failed.`
  - _intro at line ~18: To run the parallel regression tests after building but before installation, typ_
- **line 42:** `runs no more than ten tests concurrently.`
  - _intro at line ~40: The parallel regression test starts quite a few processes under your user ID. Pr_
- **line 50:** `or for a parallel test:`
  - _intro at line ~50: To run the tests after installation (see ), initialize a data directory and star_
- **line 80:** `with a `-j` limit near to or a bit more than the number of available cores.`
  - _intro at line ~80: On a modern machine with multiple CPU cores and no tight operating-system limits_

### `iii-server-administration/31-regression-tests/test-evaluation.md`

- **line 96:** `should produce only one or a few lines of differences.`
  - _intro at line ~94: The `random` test script is intended to produce random results. In very rare cas_

### `iii-server-administration/31-regression-tests/variant-comparison-files.md`

- **line 30:** `which will trigger on any machine where the output of `config.guess` matches `.*`
  - _intro at line ~28: For example: some systems lack a working `strtof` function, for which our workar_

### `iv-client-interfaces/32-libpq-c-library/command-execution-functions.md`

- **line 335:** `we would have the results:`
  - _intro at line ~333: The given name is treated like an identifier in an SQL command, that is, it is d_

### `iv-client-interfaces/32-libpq-c-library/ldap-lookup-of-connection-parameters.md`

- **line 34:** `might be queried with the following LDAP URL:`
  - _intro at line ~22: A sample LDAP entry that has been created with the LDIF file_

### `iv-client-interfaces/32-libpq-c-library/oauth-support.md`

- **line 42:** `which libpq will call when an action is required of the application. *type* desc`
  - _intro at line ~40: The behavior of the OAuth flow may be modified or replaced by a client using the_

### `iv-client-interfaces/32-libpq-c-library/pipeline-mode.md`

- **line 164:** `could be much more efficiently done with:`
  - _intro at line ~157: Pipeline mode is not useful when information from one operation is required by t_

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/internals.md`

- **line 77:** `is not copied to the output.`
  - _intro at line ~75: Note that not all SQL commands are treated in this way. For instance, an open cu_
- **line 89:** `is translated into:`
  - _intro at line ~82: Here is a complete example describing the output of the preprocessor of a file `_

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/preprocessor-directives.md`

- **line 39:** `because this file would not be subject to SQL command preprocessing.`
  - _intro at line ~37: Note that `EXEC SQL INCLUDE` is _not_ the same as:_
- **line 75:** `then `ecpg` will already do the substitution and your C compiler will never see `
  - _intro at line ~61: Of course you can continue to use the C versions `#define` and `#undef` in your _

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/using-host-variables.md`

- **line 292:** `is converted into:`
  - _intro at line ~292: The other way is using the `VARCHAR` type, which is a special type provided by E_
- **line 422:** `is converted into:`
  - _intro at line ~422: The handling of the `bytea` type is similar to that of `VARCHAR`. The definition_
- **line 693:** `would not work correctly in this case, because you cannot map an array type colu`
  - _intro at line ~37: Note again that_
- **line 844:** `has the same effect as`
  - _intro at line ~828: For example,_

### `v-server-programming/36-extending-sql/c-language-functions.md`

- **line 256:** `must appear in the same source file. (Conventionally, it\'s written just before `
  - _intro at line ~250: The version-1 calling convention relies on macros to suppress most of the comple_
- **line 639:** `passing the same `fcinfo` struct passed to the calling function itself. (This of`
  - _intro at line ~635: Several helper functions are available for setting up the needed `TupleDesc`. Th_
- **line 658:** `to get a TupleDesc based on a type OID.`
  - _intro at line ~652: Older, now-deprecated functions for obtaining `TupleDesc`s are:_
- **line 677:** `to build a HeapTuple given user data in Datum form.`
  - _intro at line ~677: When working with Datums, use:_
- **line 683:** `to build a HeapTuple given user data in C string form. `values` is an array of C`
  - _intro at line ~683: When working with C strings, use:_
- **line 693:** `to convert a HeapTuple into a valid Datum.`
  - _intro at line ~693: Once you have built a tuple to return from your function, it must be converted i_

### `v-server-programming/36-extending-sql/extension-building-infrastructure.md`

- **line 145:** `then `postgresql` will be appended to the directory names, installing the contro`
  - _intro at line ~138: You can select a separate directory prefix in which to install your extension's _

### `v-server-programming/36-extending-sql/function-overloading.md`

- **line 20:** `it is not immediately clear which function would be called with some trivial inp`
  - _intro at line ~17: When creating a family of overloaded functions, one should be careful not to cre_

### `v-server-programming/36-extending-sql/interfacing-extensions-to-indexes.md`

- **line 736:** `but there is no need to do so when the operators take the same data type we are `
  - _intro at line ~734: We could have written the operator entries more verbosely, as in:_
- **line 930:** `where `float_ops` is the built-in operator family that includes operations on `f`
  - _intro at line ~928: While search operators have to return Boolean results, ordering operators usuall_
- **line 942:** `can be satisfied exactly by a B-tree index on the integer column.`
  - _intro at line ~940: Normally, declaring an operator as a member of an operator class (or family) mea_

### `v-server-programming/36-extending-sql/operator-optimization-information.md`

- **line 54:** `for the current operator and a particular constant value.`
  - _intro at line ~52: The `RESTRICT` clause, if provided, names a restriction selectivity estimation f_
- **line 80:** `for the current operator.`
  - _intro at line ~78: The `JOIN` clause, if provided, names a join selectivity estimation function for_

### `v-server-programming/36-extending-sql/query-language-sql-functions.md`

- **line 75:** `but this will not work:`
  - _intro at line ~73: SQL function arguments can only be used as data values, not as identifiers. Thus_
- **line 155:** `which adjusts the balance and returns the new balance.`
  - _intro at line ~133: In practice one would probably like a more useful result from the function than _
- **line 261:** `or by calling it as a table function:`
  - _intro at line ~257: We could call this function directly either by using it in a value expression:_
- **line 347:** `but not having to bother with the separate composite type definition is often ha`
  - _intro at line ~318: An alternative way of describing a function's results is to define it with _outp_
- **line 429:** `but not these:`
  - _intro at line ~431: The array element parameters generated from a variadic parameter are treated as _

### `v-server-programming/36-extending-sql/user-defined-aggregates.md`

- **line 29:** `which we might use like this:`
  - _intro at line ~22: If we define an aggregate that does not use a final function, we have an aggrega_
- **line 207:** `the parser will see this as a single aggregate function argument and three sort `
  - _intro at line ~205: Variadic aggregates are easily misused in connection with the `ORDER BY` option _

### `v-server-programming/39-the-rule-system/materialized-views.md`

- **line 17:** `are that the materialized view cannot subsequently be directly updated and that `
  - _intro at line ~11: Materialized views in PostgreSQL use the rule system like views do, but persist _

### `v-server-programming/39-the-rule-system/rules-on-insert-update-and-delete.md`

- **line 232:** `and that qualification will never be true.`
  - _intro at line ~222: The substitutions and the added qualifications ensure that, if the original quer_
- **line 251:** `being generated by the rule.`
  - _intro at line ~114: It will also work if the original query modifies multiple rows. So if someone is_
- **line 377:** `and check the results:`
  - _intro at line ~334: Now assume that once in a while, a pack of shoelaces arrives at the shop and a b_
- **line 558:** `and do it this way:`
  - _intro at line ~559: Now we want to set it up so that mismatching shoelaces that are not in stock are_

### `v-server-programming/39-the-rule-system/rules-versus-triggers.md`

- **line 91:** `which results in the following executing plan for the command added by the rule:`
  - _intro at line ~54: With the next delete we want to get rid of all the 2000 computers where the `hos_

### `v-server-programming/39-the-rule-system/views-and-the-rule-system.md`

- **line 15:** `is very nearly the same thing as`
  - _intro at line ~13: Views in PostgreSQL are implemented using the rule system. A view is basically a_
- **line 153:** `and this is given to the rule system.`
  - _intro at line ~148: This is the simplest `SELECT` you can do on our views, so we take this opportuni_
- **line 272:** `are nearly identical.`
  - _intro at line ~268: There are only a few differences between a query tree for a `SELECT` and one for_
- **line 288:** `and thus the executor run over the join will produce exactly the same result set`
  - _intro at line ~286: The consequence is, that both query trees result in similar execution plans: The_

### `v-server-programming/41-pl-pgsql-sql-procedural-language/basic-statements.md`

- **line 252:** `will never succeed if `keyvalue` is null, because the result of using the equali`
  - _intro at line ~252: As always, care must be taken to ensure that null values in a query do not deliv_
- **line 270:** `because it would break if the contents of `newvalue` happened to contain `$$`.`
  - _intro at line ~223: Note that dollar quoting is only useful for quoting fixed text. It would be a ve_

### `v-server-programming/41-pl-pgsql-sql-procedural-language/declarations.md`

- **line 197:** `will work, automatically promoting the integer inputs to numeric.`
  - _intro at line ~163: In practice it might be more useful to declare a polymorphic function using the _

### `v-server-programming/41-pl-pgsql-sql-procedural-language/expressions.md`

- **line 18:** `what happens behind the scenes is equivalent to`
  - _intro at line ~16: All expressions used in PL/pgSQL statements are processed using the server's mai_
- **line 31:** `since the *expression* between `IF` and `THEN` is parsed as though it were `SELE`
  - _intro at line ~29: Since an _expression_ is converted to a `SELECT` command, it can contain the sam_

### `v-server-programming/41-pl-pgsql-sql-procedural-language/tips-for-developing-in-pl-pgsql.md`

- **line 67:** `which is exactly what the PL/pgSQL parser would see in either case.`
  - _intro at line ~61: For string literals inside the function body, for example:_
- **line 80:** `being careful that any dollar-quote delimiters around this are not just `$$`.`
  - _intro at line ~82: In the dollar-quoting approach, you'd write:_
- **line 113:** `where we assume we only need to put single quote marks into `a_output`, because `
  - _intro at line ~112: In the dollar-quoting approach, this becomes:_

### `v-server-programming/42-pl-tcl-tcl-procedural-language/database-access-from-pl-tcl.md`

- **line 23:** `will set the Tcl variable `$cnt` to the number of rows in the pg_proc system cat`
  - _intro at line ~21: If the command is a `SELECT` statement and no _loop-body_ script is given, then _
- **line 80:** `which can be formed in PL/Tcl using:`
  - _intro at line ~70: Doubles all occurrences of single quote and backslash characters in the given st_

### `v-server-programming/42-pl-tcl-tcl-procedural-language/pl-tcl-functions-and-arguments.md`

- **line 104:** `and here is one returning a composite type:`
  - _intro at line ~98: PL/Tcl functions can return sets. To do this, the Tcl code should call `return_n_

### `v-server-programming/43-pl-perl-perl-procedural-language/pl-perl-functions-and-arguments.md`

- **line 230:** `at the top of the function body.`
  - _intro at line ~228: For permanent use in specific functions you can simply put:_

### `v-server-programming/44-pl-python-python-procedural-language/pl-python-functions.md`

- **line 42:** `assuming that 23456 is the OID assigned to the function by PostgreSQL.`
  - _intro at line ~26: For example, a function to return the greater of two integers can be defined as:_
- **line 55:** `because assigning to `x` makes `x` a local variable for the entire block, and so`
  - _intro at line ~48: The arguments are set as global variables. Because of the scoping rules of Pytho_

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 128:** `at most 5 rows would be inserted, since execution would stop after the fifth `RE`
  - _intro at line ~115: If `count` is zero then the command is executed for all rows that it applies to._

### `vi-reference/client-apps/pg-restore.md`

- **line 396:** `could be used as input to pg_restore and would only restore items 10 and 6, in t`
  - _intro at line ~390: Lines in the file can be commented out, deleted, and reordered. For example:_

### `vi-reference/client-apps/pgbench.md`

- **line 50:** `where *dbname* is the name of the already-created database to test in. (You may `
  - _intro at line ~48: The default TPC-B-like transaction test requires specific tables to be set up be_

### `vi-reference/client-apps/psql.md`

- **line 1041:** `results in sending the three SQL commands to the server in a single request, whe`
  - _intro at line ~1035: Normally, psql will dispatch an SQL command to the server as soon as it reaches _
- **line 1175:** `in `~/.psqlrc` will cause psql to maintain a separate history for each database.`
  - _intro at line ~1173: The file name that will be used to store the history list. If unset, the file na_

### `vi-reference/server-apps/pg-archivecleanup.md`

- **line 84:** `where the archive directory is physically located on the standby server, so that`
  - _intro at line ~23: On Linux or Unix systems, you might use:_

### `vi-reference/server-apps/postgres.md`

- **line 225:** `depending on your system.`
  - _intro at line ~223: A failure message suggesting that another server is already running should be ch_

### `vi-reference/sql-commands/create-aggregate.md`

- **line 143:** `must be equivalent to:`
  - _intro at line ~141: Aggregates that behave like `MIN` or `MAX` can sometimes be optimized by looking_

### `vi-reference/sql-commands/create-cast.md`

- **line 32:** `converts the integer constant 42 to type `float8` by invoking a previously speci`
  - _intro at line ~30: `CREATE CAST` defines a new cast. A cast specifies how to perform a conversion b_
- **line 52:** `will be allowed if the cast from type `integer` to type `text` is marked `AS ASS`
  - _intro at line ~50: If the cast is marked `AS ASSIGNMENT` then it can be invoked implicitly when ass_

### `vi-reference/sql-commands/create-function.md`

- **line 170:** `or a block`
  - _intro at line ~168: The body of a `LANGUAGE SQL` function. This can either be a single statement_

### `vi-reference/sql-commands/create-sequence.md`

- **line 37:** `to examine the parameters and current state of a sequence.`
  - _intro at line ~35: Although you cannot update a sequence directly, you can use a query like:_

### `vi-reference/sql-commands/create-view.md`

- **line 93:** `is bad form because the column name defaults to `?column?`; also, the column dat`
  - _intro at line ~93: Be careful that the names and types of the view's columns will be assigned the w_

### `vi-reference/sql-commands/drop-function.md`

- **line 65:** `which refers to a function with zero arguments, whereas the first variant can re`
  - _intro at line ~59: If the function name is unique in its schema, it can be referred to without an a_

### `vi-reference/sql-commands/drop-procedure.md`

- **line 76:** `any one of these commands would work to drop it:`
  - _intro at line ~74: Given this procedure definition:_

### `vi-reference/sql-commands/select.md`

- **line 372:** `retrieves the most recent weather report for each location.`
  - _intro at line ~368: `SELECT DISTINCT ON ( expression [, ...] )` keeps only the first row of each set_
- **line 537:** `would fail to preserve the `FOR UPDATE` lock after the `ROLLBACK TO`.`
  - _intro at line ~531: Previous releases failed to preserve a lock which is upgraded by a later savepoi_
- **line 556:** `is equivalent to`
  - _intro at line ~554: The command_

### `vii-internals/54-frontend-backend-protocol/message-flow.md`

- **line 180:** `then the divide-by-zero failure in the `SELECT` will force rollback of the first`
  - _intro at line ~176: When a simple Query message contains more than one SQL statement (separated by s_
- **line 230:** `then none of the statements would get run, resulting in the visible difference t`
  - _intro at line ~189: Another behavior of note is that initial lexical and syntactic analysis is done _

### `vii-internals/55-postgresql-coding-conventions/formatting.md`

- **line 48:** `to make them show tabs appropriately.`
  - _intro at line ~45: The text browsing tools more and less can be invoked as:_

### `vii-internals/55-postgresql-coding-conventions/miscellaneous-coding-conventions.md`

- **line 29:** `or when the macro would be very long.`
  - _intro at line ~27: Both macros with arguments and `static inline` functions may be used. The latter_

### `vii-internals/55-postgresql-coding-conventions/reporting-errors-within-the-server.md`

- **line 106:** `is exactly equivalent to:`
  - _intro at line ~104: There is an older function `elog` that is still heavily used. An `elog` call:_

### `vii-internals/56-native-language-support/for-the-translator.md`

- **line 106:** `which will create a new blank message catalog file (the pot file you started wit`
  - _intro at line ~104: As the underlying program or library changes, messages might be changed or added_

### `vii-internals/65-built-in-index-access-methods/sp-gist-indexes.md`

- **line 713:** `attType is passed in order to support polymorphic index operator classes; for or`
  - _intro at line ~695: The SQL declaration of the function must look like this:_
- **line 822:** `nTuples is the number of leaf tuples provided. datums is an array of their datum`
  - _intro at line ~799: The SQL declaration of the function must look like this:_

### `vii-internals/69-how-the-planner-uses-statistics/row-estimation-examples.md`

- **line 64:** `that is, one whole bucket plus a linear fraction of the second, divided by the n`
  - _intro at line ~35: Let's move on to an example with a range condition in its `WHERE` clause:_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-12-dict-int-example-full-text-search-dictionary-for-integers.md`

- **line 40:** `but real-world usage will involve including it in a text search configuration as`
  - _intro at line ~35: To test the dictionary, you can try_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-35-pg-trgm-support-for-similarity-of-text-using-trigram-matching.md`

- **line 289:** `where documents is a table that has a text field bodytext that we wish to search`
  - _intro at line ~286: The first step is to generate an auxiliary table containing all the unique words_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-48-unaccent-a-text-search-dictionary-which-removes-diacritics.md`

- **line 61:** `or create new dictionaries based on the template.`
  - _intro at line ~59: Installing the `unaccent` extension creates a text search template `unaccent` an_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-50-xml2-xpath-querying-and-xslt-functionality.md`

- **line 186:** `as a more complicated example. Of course, you could wrap all of this in a view f`
  - _intro at line ~180: The calling `SELECT` statement doesn't necessarily have to be just `SELECT *` it_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/index.md`

- **line 28:** `once you have a PostgreSQL server running.`
  - _intro at line ~26: When building from the source distribution, these optional components are not bu_

## WOULD_FIX (15)

_Still needs fixing — intro absent, but repair is known_

### `ii-the-sql-language/07-queries/table-expressions.md`

- **line 129:** `then we get the following results for the various joins:`
  - _INSERT before line 117: To put this together, assume we have tables `t1`:_

### `ii-the-sql-language/08-data-types/numeric-types.md`

- **line 267:** `is equivalent to specifying:`
  - _INSERT before line 268: The data types `smallserial`, `serial` and `bigserial` are not true types, but m_

### `ii-the-sql-language/11-indexes/index-types.md`

- **line 47:** `which finds the ten places closest to a given target point.`
  - _INSERT before line 47: GiST indexes are also capable of optimizing "nearest-neighbor" searches, such as_

### `ii-the-sql-language/13-concurrency-control/transaction-isolation.md`

- **line 212:** `because a repeatable read transaction cannot modify or lock rows changed by othe`
  - _INSERT before line 212: `UPDATE`, `DELETE`, `MERGE`, `SELECT FOR UPDATE`, and `SELECT FOR SHARE` command_
- **line 260:** `and obtains the result 300, which it inserts in a new row with class`= 1`.`
  - _INSERT before line 248: As an example, consider a table `mytab`, initially containing:_

### `iii-server-administration/19-server-configuration/client-connection-defaults.md`

- **line 293:** `or, in a Windows environment:`
  - _INSERT before line 293: The value for `dynamic_library_path` must be a list of absolute directory paths _
- **line 308:** `or, in a Windows environment:`
  - _INSERT before line 310: The value for `extension_control_path` must be a list of absolute directory path_

### `iii-server-administration/22-managing-databases/template-databases.md`

- **line 28:** `from the SQL environment, or:`
  - _INSERT before line 28: To create a database by copying `template0`, use:_

### `iii-server-administration/25-backup-and-restore/continuous-archiving-and-point-in-time-recovery-pitr.md`

- **line 65:** `which will copy archivable WAL segments to the directory `/mnt/server/archivedir`
  - _INSERT before line 64: In `archive_command`, `%p` is replaced by the path name of the file to archive, _

### `iv-client-interfaces/32-libpq-c-library/database-connection-control-functions.md`

- **line 219:** `which libpq will then call *instead of* its default `PQdefaultSSLKeyPassHook_Ope`
  - _INSERT before line 219: `PQsetSSLKeyPassHook_OpenSSL` lets an application override libpq's default handl_

### `v-server-programming/36-extending-sql/c-language-functions.md`

- **line 670:** `if you plan to work with C strings.`
  - _INSERT before line 666: Once you have a `TupleDesc`, call:_

### `v-server-programming/36-extending-sql/packaging-related-objects-into-an-extension.md`

- **line 185:** `and then make sure that standard_entry is true only in the rows created by the e`
  - _INSERT before line 169: When the second argument of `pg_extension_config_dump` is an empty string, the e_

### `v-server-programming/41-pl-pgsql-sql-procedural-language/tips-for-developing-in-pl-pgsql.md`

- **line 21:** `and then immediately issue SQL commands to test the function.`
  - _INSERT before line 21: While running psql, you can load or reload such a function definition file with:_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-1-amcheck-tools-to-verify-table-and-index-consistency.md`

- **line 86:** `in an interactive psql session before running a verification query will display `
  - _INSERT before line 86: `bt_index_check` and `bt_index_parent_check` both output log messages about the _

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-43-tablefunc-functions-that-return-tables-crosstab-and-others.md`

- **line 112:** `which we wish to display like`
  - _INSERT before line 105: The `crosstab` function is used to produce "pivot" displays, wherein data is lis_

## FALSE_POS (134)

_Not a dropped sentence — refpurpose / synopsis / screen element_

### `ii-the-sql-language/04-sql-syntax/lexical-structure.md`

- **line 433:** `where the comment begins with `/*` and extends to the matching occurrence of `*/`
  - _programlisting_

### `ii-the-sql-language/07-queries/with-queries-common-table-expressions.md`

- **line 314:** `so that the parent query\'s restrictions can be applied directly to scans of big`
  - _programlisting_

### `ii-the-sql-language/08-data-types/numeric-types.md`

- **line 91:** `without any precision or scale creates an "unconstrained numeric" column in whic`
  - _programlisting_

### `ii-the-sql-language/08-data-types/text-search-types.md`

- **line 138:** `which will match the stemmed form of `postgraduate`.`
  - _programlisting_

### `ii-the-sql-language/10-type-conversion/overview.md`

- **line 26:** `has two literal constants, of type `text` and `point`.`
  - _screen_

### `ii-the-sql-language/11-indexes/index-only-scans-and-covering-indexes.md`

- **line 66:** `the uniqueness condition applies to just column `x`, not to the combination of ``
  - _programlisting_

### `iii-server-administration/18-server-setup-and-operation/managing-kernel-resources.md`

- **line 292:** `or placing an equivalent entry in `/etc/sysctl.conf`.`
  - _programlisting_

### `iii-server-administration/18-server-setup-and-operation/starting-the-database-server.md`

- **line 131:** `probably means your kernel\'s limit on the size of shared memory is smaller than`
  - _screen_

### `iii-server-administration/23-localization/collation-support.md`

- **line 59:** `the comparison is performed using `fr_FR` rules, because the explicit collation `
  - _programlisting_
- **line 64:** `the parser cannot determine which collation to apply, since the a and b columns `
  - _programlisting_
- **line 78:** `does not result in an error, because the `||` operator does not care about colla`
  - _programlisting_

### `iii-server-administration/24-routine-database-maintenance-tasks/routine-vacuuming.md`

- **line 316:** `where the vacuum max threshold is [autovacuum_vacuum_max_threshold (integer)`
  - _programlisting_
- **line 331:** `where the vacuum insert base threshold is [autovacuum_vacuum_insert_threshold (i`
  - _programlisting_

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/embedded-sql-commands.md`

- **line 13:** `allocate an SQL descriptor area`
  - _refpurpose_
- **line 45:** `establish a database connection`
  - _refpurpose_
- **line 180:** `deallocate an SQL descriptor area`
  - _refpurpose_
- **line 210:** `define a cursor`
  - _refpurpose_
- **line 270:** `declare SQL statement identifier`
  - _refpurpose_
- **line 392:** `terminate a database connection`
  - _refpurpose_
- **line 441:** `dynamically prepare and execute a statement`
  - _refpurpose_
- **line 481:** `get information from an SQL descriptor area`
  - _refpurpose_
- **line 609:** `open a dynamic cursor`
  - _refpurpose_
- **line 666:** `prepare a statement for execution`
  - _refpurpose_
- **line 719:** `set the autocommit behavior of the current session`
  - _refpurpose_
- **line 735:** `select a database connection`
  - _refpurpose_
- **line 769:** `set information in an SQL descriptor area`
  - _refpurpose_
- **line 841:** `define a new data type`
  - _refpurpose_
- **line 945:** `define a variable`
  - _refpurpose_
- **line 984:** `specify the action to be taken when an SQL statement causes a specific class con`
  - _refpurpose_

### `v-server-programming/36-extending-sql/c-language-functions.md`

- **line 792:** `to set up for using the FuncCallContext.`
  - _programlisting_
- **line 798:** `to return it to the caller. (`result` must be of type `Datum`, either a single v`
  - _programlisting_
- **line 802:** `to clean up and end the SRF.`
  - _programlisting_

### `v-server-programming/36-extending-sql/query-language-sql-functions.md`

- **line 211:** `but this usage is deprecated since it\'s easy to get confused. (See [Using Compo`
  - _screen_

### `v-server-programming/39-the-rule-system/rules-on-insert-update-and-delete.md`

- **line 240:** `four rows in fact get updated (`sl1`, `sl2`, `sl3`, and `sl4`).`
  - _programlisting_
- **line 421:** `and throws away the original `INSERT` on `shoelace_ok`.`
  - _programlisting_

### `v-server-programming/41-pl-pgsql-sql-procedural-language/expressions.md`

- **line 22:** `and then this prepared statement is `EXECUTE`d for each execution of the `IF` st`
  - _programlisting_

### `v-server-programming/42-pl-tcl-tcl-procedural-language/database-access-from-pl-tcl.md`

- **line 31:** `will print a log message for every row of `pg_class`. This feature works similar`
  - _programlisting_
- **line 72:** `where the Tcl variable `val` actually contains `doesn't`. This would result in t`
  - _programlisting_
- **line 76:** `which would cause a parse error during `spi_exec` or `spi_prepare`. To work prop`
  - _programlisting_

### `v-server-programming/44-pl-python-python-procedural-language/database-access.md`

- **line 25:** `returns up to 5 rows from `my_table`. If `my_table` has a column `my_column`, it`
  - _programlisting_

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 16:** `connect a C function to the SPI manager`
  - _refpurpose_
- **line 18:** `int SPI_connect(void)`
  - _synopsis_
- **line 60:** `disconnect a C function from the SPI manager`
  - _refpurpose_
- **line 62:** `int SPI_finish(void)`
  - _synopsis_
- **line 90:** `int SPI_execute(const char \*`
  - _synopsis_
- **line 123:** `inserts all rows from bar, ignoring the `count` parameter.`
  - _programlisting_
- **line 260:** `execute a read/write command`
  - _refpurpose_
- **line 262:** `int SPI_exec(const char \*`
  - _synopsis_
- **line 297:** `execute a command with out-of-line parameters`
  - _refpurpose_
- **line 373:** `execute a command with out-of-line parameters`
  - _refpurpose_
- **line 707:** `int SPI_getargcount(SPIPlanPtr`
  - _synopsis_
- **line 736:** `return the data type OID for an argument of a statement prepared by`
  - _refpurpose_
- **line 1032:** `int SPI_execp(SPIPlanPtr`
  - _synopsis_
- **line 1085:** `set up a cursor using a statement created with`
  - _refpurpose_
- **line 1156:** `set up a cursor using a query and parameters`
  - _refpurpose_
- **line 1246:** `set up a cursor using parameters`
  - _refpurpose_
- **line 1303:** `set up a cursor using a query string and parameters`
  - _refpurpose_
- **line 1372:** `find an existing cursor by name`
  - _refpurpose_
- **line 1408:** `fetch some rows from a cursor`
  - _refpurpose_
- **line 1457:** `move a cursor`
  - _refpurpose_
- **line 1502:** `fetch some rows from a cursor`
  - _refpurpose_
- **line 1553:** `move a cursor`
  - _refpurpose_
- **line 1604:** `close a cursor`
  - _refpurpose_
- **line 1632:** `save a prepared statement`
  - _refpurpose_
- **line 1634:** `int SPI_keepplan(SPIPlanPtr`
  - _synopsis_
- **line 1668:** `save a prepared statement`
  - _refpurpose_
- **line 1715:** `make an ephemeral named relation available by name in SPI queries`
  - _refpurpose_
- **line 1765:** `remove an ephemeral named relation from the registry`
  - _refpurpose_
- **line 1815:** `make ephemeral trigger data available in SPI queries`
  - _refpurpose_

### `v-server-programming/45-server-programming-interface/interface-support-functions.md`

- **line 18:** `determine the column name for the specified column number`
  - _screen_
- **line 55:** `determine the column number for the specified column name`
  - _screen_
- **line 57:** `int SPI_fnumber(TupleDesc`
  - _synopsis_
- **line 95:** `return the string value of the specified column`
  - _refpurpose_
- **line 141:** `return the binary value of the specified column`
  - _refpurpose_
- **line 198:** `return the data type name of the specified column`
  - _refpurpose_
- **line 235:** `return the data type`
  - _refpurpose_
- **line 277:** `return the name of the specified relation`
  - _refpurpose_
- **line 307:** `return the namespace of the specified relation`
  - _refpurpose_
- **line 339:** `return error code as string`
  - _refpurpose_

### `v-server-programming/45-server-programming-interface/memory-management.md`

- **line 30:** `allocate memory in the upper executor context`
  - _refpurpose_
- **line 63:** `reallocate memory in the upper executor context`
  - _refpurpose_
- **line 103:** `free memory in the upper executor context`
  - _refpurpose_
- **line 105:** `void SPI_pfree(void \*`
  - _synopsis_
- **line 132:** `make a copy of a row in the upper executor context`
  - _refpurpose_
- **line 167:** `prepare to return a tuple as a Datum`
  - _refpurpose_
- **line 211:** `create a row by replacing selected fields of a given row`
  - _refpurpose_
- **line 297:** `free a row allocated in the upper executor context`
  - _refpurpose_
- **line 299:** `void SPI_freetuple(HeapTuple`
  - _synopsis_
- **line 326:** `free a row set created by`
  - _refpurpose_
- **line 332:** `void SPI_freetuptable(SPITupleTable \*`
  - _synopsis_
- **line 364:** `free a previously saved prepared statement`
  - _refpurpose_
- **line 366:** `int SPI_freeplan(SPIPlanPtr`
  - _synopsis_

### `v-server-programming/45-server-programming-interface/transaction-management.md`

- **line 26:** `void SPI_commit(void)`
  - _synopsis_
- **line 49:** `abort the current transaction`
  - _refpurpose_
- **line 51:** `void SPI_rollback(void)`
  - _synopsis_

### `vi-reference/client-apps/psql.md`

- **line 1282:** `would query the table `my_table`.`
  - _programlisting_
- **line 1381:** `results in a boldfaced (`1;`) yellow-on-black (`33;40`) prompt on VT100-compatib`
  - _programlisting_

### `vi-reference/sql-commands/create-type.md`

- **line 393:** `which would allow a box value\'s component numbers to be accessed by subscriptin`
  - _programlisting_

### `vi-reference/sql-commands/select.md`

- **line 526:** `will lock only rows having `col1 = 5`, even though that condition is not textual`
  - _programlisting_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-11-dblink-connect-to-other-postgresql-databases.md`

- **line 32:** `opens a persistent connection to a remote database`
  - _refpurpose_
- **line 145:** `opens a persistent connection to a remote database, insecurely`
  - _refpurpose_
- **line 168:** `closes a persistent connection to a remote database`
  - _refpurpose_
- **line 209:** `executes a query in a remote database`
  - _refpurpose_
- **line 211:** `dblink(text connname, text sql \[, bool fail_on_error\]) returns setof record db`
  - _synopsis_
- **line 346:** `executes a command in a remote database`
  - _refpurpose_
- **line 419:** `opens a cursor in a remote database`
  - _refpurpose_
- **line 475:** `returns rows from an open cursor in a remote database`
  - _refpurpose_
- **line 563:** `closes a cursor in a remote database`
  - _refpurpose_
- **line 641:** `gets last error message on the named connection`
  - _refpurpose_
- **line 676:** `sends an async query to a remote database`
  - _refpurpose_
- **line 713:** `checks if connection is busy with an async query`
  - _refpurpose_
- **line 744:** `retrieve async notifications on a connection`
  - _refpurpose_
- **line 794:** `gets an async query result`
  - _refpurpose_
- **line 895:** `cancels any active query on the named connection`
  - _refpurpose_
- **line 978:** `builds an INSERT statement using a local tuple, replacing the primary key field `
  - _refpurpose_
- **line 1031:** `builds a DELETE statement using supplied values for primary key field values`
  - _refpurpose_
- **line 1081:** `builds an UPDATE statement using a local tuple, replacing the primary key field `
  - _refpurpose_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-16-fuzzystrmatch-determine-string-similarities-and-distance.md`

- **line 24:** `soundex(text) returns text difference(text, text) returns int`
  - _synopsis_
- **line 150:** `levenshtein(source text, target text, ins_cost int, del_cost int, sub_cost int) `
  - _synopsis_
- **line 193:** `metaphone(source text, max_output_length int) returns text`
  - _synopsis_
- **line 211:** `dmetaphone(source text) returns text dmetaphone_alt(source text) returns text`
  - _synopsis_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-26-pgcrypto-cryptographic-functions.md`

- **line 18:** `digest(data text, type text) returns bytea digest(data bytea, type text) returns`
  - _synopsis_
- **line 33:** `hmac(data text, key text, type text) returns bytea hmac(data bytea, key bytea, t`
  - _synopsis_
- **line 117:** `crypt(password text, salt text) returns text`
  - _synopsis_
- **line 633:** `encrypt(data bytea, key bytea, type text) returns bytea decrypt(data bytea, key `
  - _synopsis_
- **line 674:** `fips_mode() returns boolean`
  - _synopsis_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-31-pgrowlocks-show-a-table-s-row-locking-information.md`

- **line 14:** `pgrowlocks(text) returns setof record`
  - _synopsis_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-43-tablefunc-functions-that-return-tables-crosstab-and-others.md`

- **line 73:** `normal_rand(int numvals, float8 mean, float8 stddev) returns setof float8`
  - _synopsis_
- **line 252:** `crosstab(text source_sql, text category_sql)`
  - _synopsis_
- **line 389:** `connectby(text relname, text keyid_fld, text parent_keyid_fld \[, text orderby_f`
  - _synopsis_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-50-xml2-xpath-querying-and-xslt-functionality.md`

- **line 99:** `xpath_table(text key, text document, text relation, text xpaths, text criteria) `
  - _synopsis_
- **line 245:** `xslt_process(text document, text stylesheet, text paramlist) returns text`
  - _synopsis_

### `viii-appendixes/g-additional-supplied-programs/g-1-client-applications.md`

- **line 20:** `resolve OIDs and file nodes in a`
  - _refpurpose_
- **line 258:** `remove orphaned large objects from a`
  - _refpurpose_

## NO_XML_MATCH (241)

_No XML para match — needs manual review during content pass_

### `ii-the-sql-language/04-sql-syntax/lexical-structure.md`

- **line 60:** `delimited identifier or quoted identifier.`

### `ii-the-sql-language/05-data-definition/dependency-tracking.md`

- **line 65:** `then the function\'s dependency on the my_colors table will be known and enforce`

### `ii-the-sql-language/07-queries/table-expressions.md`

- **line 121:** `and `t2`:`

### `ii-the-sql-language/08-data-types/date-time-types.md`

- **line 422:** `is a `timestamp without time zone`, while`
- **line 426:** `is a `timestamp with time zone`. PostgreSQL never examines the content of a lite`

### `ii-the-sql-language/08-data-types/object-identifier-types.md`

- **line 260:** `is *not recommended*, because it will fail for tables that are outside your sear`

### `ii-the-sql-language/08-data-types/text-search-types.md`

- **line 131:** `because `postgres` gets stemmed to `postgr`:`

### `ii-the-sql-language/09-functions-and-operators/date-time-functions-and-operators.md`

- **line 821:** `date_trunc(*field*, *source* \[, *time_zone*\]) *source* is a value expression o`
- **line 853:** `date_bin(*stride*, *source*, *origin*) *source* is a value expression of type `t`

### `ii-the-sql-language/09-functions-and-operators/json-functions-and-operators.md`

- **line 34:** `and Operators shows the operators that are available for use with JSON data type`

### `ii-the-sql-language/11-indexes/index-only-scans-and-covering-indexes.md`

- **line 47:** `covering index, which is an index specifically designed to include the columns n`

### `ii-the-sql-language/12-full-text-search/dictionaries.md`

- **line 232:** `where the colon (`:`) symbol acts as a delimiter between a phrase and its replac`
- **line 247:** `matches `a one the two` and `the one a two`; both would be replaced by `swsw`.`

### `ii-the-sql-language/14-performance-tips/using-explain.md`

- **line 341:** `subplans, which arise from sub-`SELECT`s in the original query.`

### `iii-server-administration/17-installation-from-source-code/platform-specific-notes.md`

- **line 78:** `macOS\'s "System Integrity Protection" (SIP) feature breaks `make check`, becaus`

### `iii-server-administration/17-installation-from-source-code/post-installation-setup.md`

- **line 18:** `or in `csh` or `tcsh`:`

### `iii-server-administration/18-server-setup-and-operation/starting-the-database-server.md`

- **line 142:** `does *not* mean you\'ve run out of disk space.`

### `iii-server-administration/19-server-configuration/error-reporting-and-logging.md`

- **line 31:** `to the syslog daemon\'s configuration file to make it work.`

### `iii-server-administration/19-server-configuration/write-ahead-log.md`

- **line 48:** `synchronous_commit Modes summarizes the capabilities of the `synchronous_commit``

### `iii-server-administration/23-localization/collation-support.md`

- **line 54:** `the `<` comparison is performed according to `de_DE` rules, because the expressi`

### `iii-server-administration/25-backup-and-restore/sql-dump.md`

- **line 73:** `pg_dumpall works by emitting commands to re-create roles, tablespaces, and empty`

### `iii-server-administration/26-high-availability-load-balancing-and-replication/hot-standby.md`

- **line 257:** `pg_locks will show locks held by backends, as normal. pg_locks also shows a virt`

### `iii-server-administration/27-monitoring-database-activity/the-cumulative-statistics-system.md`

- **line 4225:** `pg_stat_io can be used to inform database tuning. For example:`

### `iii-server-administration/31-regression-tests/test-coverage-examination.md`

- **line 26:** `instead of `make coverage-html`, which will produce `.gcov` output files for eac`

### `iv-client-interfaces/32-libpq-c-library/asynchronous-notification.md`

- **line 13:** `libpq applications submit `LISTEN`, `UNLISTEN`, and `NOTIFY` commands as ordinar`

### `iv-client-interfaces/32-libpq-c-library/event-system.md`

- **line 8:** `libpq\'s event system is designed to notify registered event handlers about inte`

### `iv-client-interfaces/32-libpq-c-library/index.md`

- **line 6:** `libpq is the C application programmer\'s interface to PostgreSQL. libpq is a set`

### `iv-client-interfaces/33-large-objects/example-program.md`

- **line 8:** `example is a sample program which shows how the large object interface in libpq `

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/embedded-sql-commands.md`

- **line 332:** `obtain information about a prepared statement or result set`

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/large-objects.md`

- **line 15:** `example shows an example program that illustrates how to create, write, and read`

### `v-server-programming/36-extending-sql/c-language-functions.md`

- **line 787:** `to initialize the FuncCallContext.`

### `v-server-programming/36-extending-sql/interfacing-extensions-to-indexes.md`

- **line 896:** `it is not sufficient to know how to order by `x`; the database must also underst`

### `v-server-programming/36-extending-sql/query-language-sql-functions.md`

- **line 174:** `since the `integer` sum can be implicitly cast to `float8`. (See [Type Conversio`

### `v-server-programming/37-triggers/writing-trigger-functions-in-c.md`

- **line 26:** `struct TriggerData is defined in `commands/trigger.h`:`
- **line 123:** `where tgname is the trigger\'s name, tgnargs is the number of arguments in tgarg`

### `v-server-programming/39-the-rule-system/views-and-the-rule-system.md`

- **line 21:** `although you can\'t actually write that, because tables are not allowed to have `

### `v-server-programming/41-pl-pgsql-sql-procedural-language/control-structures.md`

- **line 187:** `and two forms of `CASE`:`

### `v-server-programming/41-pl-pgsql-sql-procedural-language/trigger-functions.md`

- **line 78:** `example shows an example of a trigger function in PL/pgSQL.`
- **line 422:** `example shows an example of an event trigger function in PL/pgSQL.`

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 20:** `int SPI_connect_ext(int`
- **line 299:** `int SPI_execute_extended(const char \*`
- **line 375:** `int SPI_execute_with_args(const char \*`
- **line 456:** `prepare a statement, without executing it yet`
- **line 533:** `prepare a statement, without executing it yet`
- **line 592:** `prepare a statement, without executing it yet`
- **line 649:** `prepare a statement, without executing it yet`
- **line 703:** `return the number of arguments needed by a statement prepared by`
- **line 789:** `bool SPI_is_cursor_plan(SPIPlanPtr`
- **line 823:** `int SPI_execute_plan(SPIPlanPtr`
- **line 896:** `int SPI_execute_plan_extended(SPIPlanPtr`
- **line 974:** `int SPI_execute_plan_with_paramlist(SPIPlanPtr`
- **line 1030:** `execute a statement in read/write mode`
- **line 1410:** `void SPI_cursor_fetch(Portal`
- **line 1459:** `void SPI_cursor_move(Portal`
- **line 1504:** `void SPI_scroll_cursor_fetch(Portal`
- **line 1555:** `void SPI_scroll_cursor_move(Portal`
- **line 1606:** `void SPI_cursor_close(Portal`
- **line 1717:** `int SPI_register_relation(EphemeralNamedRelation`
- **line 1767:** `int SPI_unregister_relation(const char \*`
- **line 1817:** `int SPI_register_trigger_data(TriggerData \*`

### `v-server-programming/45-server-programming-interface/interface-support-functions.md`

- **line 20:** `char \* SPI_fname(TupleDesc`
- **line 97:** `char \* SPI_getvalue(HeapTuple`
- **line 200:** `char \* SPI_gettype(TupleDesc`
- **line 279:** `char \* SPI_getrelname(Relation`
- **line 309:** `char \* SPI_getnspname(Relation`
- **line 341:** `const char \* SPI_result_code_string(int`

### `v-server-programming/45-server-programming-interface/memory-management.md`

- **line 32:** `void \* SPI_palloc(Size`
- **line 65:** `void \* SPI_repalloc(void \*`
- **line 330:** `or a similar function`

### `v-server-programming/45-server-programming-interface/transaction-management.md`

- **line 28:** `void SPI_commit_and_chain(void)`
- **line 53:** `void SPI_rollback_and_chain(void)`
- **line 71:** `obsolete function`
- **line 73:** `void SPI_start_transaction(void)`

### `v-server-programming/46-background-worker-processes.md`

- **line 39:** `bgw_name and bgw_type are strings to be used in log messages, process listings a`
- **line 41:** `bgw_flags is a bitwise-or\'d bit mask indicating the capabilities that the modul`
- **line 52:** `bgw_start_time is the server state during which `postgres` should start the proc`
- **line 56:** `bgw_restart_time is the interval, in seconds, that `postgres` should wait before`
- **line 59:** `bgw_library_name is the name of a library in which the initial entry point for t`
- **line 63:** `bgw_function_name is the name of the function to use as the initial entry point `
- **line 66:** `bgw_main_arg is the `Datum` argument to the background worker main function.`
- **line 77:** `bgw_notify_pid is the PID of a PostgreSQL backend process to which the postmaste`

### `v-server-programming/47-logical-decoding/streaming-replication-protocol-interface.md`

- **line 16:** `are used to create, drop, and stream changes from a replication slot, respective`

### `vi-reference/client-apps/clusterdb.md`

- **line 36:** `clusterdb is a wrapper around the SQL command [CLUSTER](braised:ref/sql-cluster)`

### `vi-reference/client-apps/dropuser.md`

- **line 20:** `dropuser is a wrapper around the SQL command [`DROP ROLE`](#sql-droprole).`

### `vi-reference/client-apps/pg-amcheck.md`

- **line 17:** `pg_amcheck supports running [F.1. amcheck — tools to verify table and index cons`

### `vi-reference/client-apps/pg-dump.md`

- **line 119:** `pg_dump will open *njobs* + 1 connections to the database, so make sure your [ma`

### `vi-reference/client-apps/pg-dumpall.md`

- **line 18:** `pg_dumpall is a utility for writing out ("dumping") all PostgreSQL databases of `

### `vi-reference/client-apps/pg-receivewal.md`

- **line 19:** `pg_receivewal streams the write-ahead log in real time as it\'s being generated `

### `vi-reference/client-apps/pg-restore.md`

- **line 20:** `pg_restore is a utility for restoring a PostgreSQL database from an archive crea`

### `vi-reference/client-apps/pg-verifybackup.md`

- **line 16:** `pg_verifybackup is used to check the integrity of a database cluster backup take`

### `vi-reference/client-apps/psql.md`

- **line 17:** `psql is a terminal-based front-end to PostgreSQL.`
- **line 1092:** `sets the variable `foo` to the value `bar`.`
- **line 1499:** `psql is built as a "console application".`

### `vi-reference/client-apps/reindexdb.md`

- **line 63:** `reindexdb is a wrapper around the SQL command [`REINDEX`](#sql-reindex).`

### `vi-reference/client-apps/vacuumdb.md`

- **line 73:** `vacuumdb is a wrapper around the SQL command [`VACUUM`](#sql-vacuum).`

### `vi-reference/server-apps/pg-archivecleanup.md`

- **line 17:** `pg_archivecleanup is designed to be used as an `archive_cleanup_command` to clea`

### `vi-reference/server-apps/pg-createsubscriber.md`

- **line 167:** `pg_createsubscriber changes the system identifier using pg_resetwal.`

### `vi-reference/server-apps/pg-rewind.md`

- **line 32:** `pg_rewind examines the timeline histories of the source and target clusters to d`
- **line 45:** `pg_rewind requires that the target server either has the [wal_log_hints (boolean`
- **line 57:** `pg_rewind will fail immediately if it finds files it cannot write directly to. T`

### `vi-reference/server-apps/pg-test-fsync.md`

- **line 15:** `pg_test_fsync is intended to give you a reasonable idea of what the fastest [wal`
- **line 23:** `pg_test_fsync accepts the following command-line options:`

### `vi-reference/server-apps/pg-test-timing.md`

- **line 15:** `pg_test_timing is a tool to measure the timing overhead on your system and confi`
- **line 20:** `pg_test_timing accepts the following command-line options:`

### `vi-reference/server-apps/pg-upgrade.md`

- **line 22:** `pg_upgrade (formerly called pg_migrator) allows data stored in PostgreSQL data f`
- **line 318:** `pg_upgrade creates various working files, such as schema dumps, stored within `p`

### `vi-reference/server-apps/pg-waldump.md`

- **line 123:** `pg_waldump cannot read WAL files with suffix `.partial`.`

### `vi-reference/server-apps/postgres.md`

- **line 309:** `or set the environment variable `PGPORT`:`

### `vi-reference/sql-commands/alter-aggregate.md`

- **line 14:** `where aggregate_signature is:`

### `vi-reference/sql-commands/alter-database.md`

- **line 11:** `where option can be:`

### `vi-reference/sql-commands/alter-default-privileges.md`

- **line 14:** `where abbreviated_grant_or_revoke is one of:`

### `vi-reference/sql-commands/alter-domain.md`

- **line 28:** `where domain_constraint is:`

### `vi-reference/sql-commands/alter-extension.md`

- **line 14:** `where member_object is:`
- **line 45:** `and aggregate_signature is:`

### `vi-reference/sql-commands/alter-foreign-table.md`

- **line 18:** `where action is one of:`

### `vi-reference/sql-commands/alter-function.md`

- **line 20:** `where action is one of:`

### `vi-reference/sql-commands/alter-group.md`

- **line 12:** `where role_specification can be:`

### `vi-reference/sql-commands/alter-materialized-view.md`

- **line 22:** `where action is one of:`

### `vi-reference/sql-commands/alter-procedure.md`

- **line 20:** `where action is one of:`

### `vi-reference/sql-commands/alter-publication.md`

- **line 16:** `where publication_object is one of:`
- **line 21:** `and publication_drop_object is one of:`
- **line 26:** `and table_and_columns is:`

### `vi-reference/sql-commands/alter-role.md`

- **line 11:** `where option can be:`
- **line 31:** `where role_specification can be:`

### `vi-reference/sql-commands/alter-routine.md`

- **line 20:** `where action is one of:`

### `vi-reference/sql-commands/alter-table.md`

- **line 26:** `where action is one of:`
- **line 77:** `and partition_bound_spec is:`
- **line 84:** `and column_constraint is:`
- **line 99:** `and table_constraint is:`
- **line 111:** `and table_constraint_using_index is:`
- **line 117:** `index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:`
- **line 123:** `exclude_element in an EXCLUDE constraint is:`
- **line 127:** `referential_action in a FOREIGN KEY/REFERENCES constraint is:`

### `vi-reference/sql-commands/alter-type.md`

- **line 18:** `where action is one of:`

### `vi-reference/sql-commands/alter-user.md`

- **line 11:** `where option can be:`
- **line 31:** `where role_specification can be:`

### `vi-reference/sql-commands/analyze.md`

- **line 11:** `where option can be one of:`
- **line 17:** `and table_and_columns is:`

### `vi-reference/sql-commands/begin.md`

- **line 11:** `where transaction_mode is one of:`

### `vi-reference/sql-commands/cluster.md`

- **line 11:** `where option can be one of:`

### `vi-reference/sql-commands/comment.md`

- **line 56:** `where aggregate_signature is:`

### `vi-reference/sql-commands/copy.md`

- **line 18:** `where option can be one of:`

### `vi-reference/sql-commands/create-aggregate.md`

- **line 45:** `or the old syntax`

### `vi-reference/sql-commands/create-domain.md`

- **line 14:** `where domain_constraint is:`

### `vi-reference/sql-commands/create-foreign-table.md`

- **line 29:** `where column_constraint is:`
- **line 39:** `and table_constraint is:`
- **line 46:** `and like_option is:`
- **line 50:** `and partition_bound_spec is:`

### `vi-reference/sql-commands/create-group.md`

- **line 11:** `where option can be:`

### `vi-reference/sql-commands/create-publication.md`

- **line 14:** `where publication_object is one of:`
- **line 19:** `and table_and_columns is:`

### `vi-reference/sql-commands/create-role.md`

- **line 11:** `where option can be:`

### `vi-reference/sql-commands/create-rule.md`

- **line 13:** `where event can be one of:`
- **line 111:** `one `NOTIFY` event will be sent during the `UPDATE`, whether or not there are an`

### `vi-reference/sql-commands/create-schema.md`

- **line 14:** `where role_specification can be:`

### `vi-reference/sql-commands/create-table.md`

- **line 46:** `where column_constraint is:`
- **line 61:** `and table_constraint is:`
- **line 73:** `and like_option is:`
- **line 77:** `and partition_bound_spec is:`
- **line 84:** `index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:`
- **line 90:** `exclude_element in an EXCLUDE constraint is:`
- **line 94:** `referential_action in a FOREIGN KEY/REFERENCES constraint is:`

### `vi-reference/sql-commands/create-trigger.md`

- **line 18:** `where event can be one of:`

### `vi-reference/sql-commands/create-user.md`

- **line 11:** `where option can be:`

### `vi-reference/sql-commands/drop-aggregate.md`

- **line 11:** `where aggregate_signature is:`

### `vi-reference/sql-commands/drop-database.md`

- **line 11:** `where option can be:`

### `vi-reference/sql-commands/explain.md`

- **line 11:** `where option can be one of:`

### `vi-reference/sql-commands/fetch.md`

- **line 11:** `where direction can be one of:`

### `vi-reference/sql-commands/grant.md`

- **line 89:** `where role_specification can be:`

### `vi-reference/sql-commands/insert.md`

- **line 17:** `where conflict_target can be one of:`
- **line 22:** `and conflict_action is one of:`

### `vi-reference/sql-commands/lock.md`

- **line 11:** `where lockmode is one of:`

### `vi-reference/sql-commands/merge.md`

- **line 16:** `where data_source is:`
- **line 20:** `and when_clause is:`
- **line 26:** `and merge_insert is:`
- **line 32:** `and merge_update is:`
- **line 39:** `and merge_delete is:`

### `vi-reference/sql-commands/move.md`

- **line 11:** `where direction can be one of:`

### `vi-reference/sql-commands/reindex.md`

- **line 12:** `where option can be one of:`

### `vi-reference/sql-commands/revoke.md`

- **line 118:** `where role_specification can be:`

### `vi-reference/sql-commands/security-label.md`

- **line 34:** `where aggregate_signature is:`

### `vi-reference/sql-commands/select.md`

- **line 24:** `where from_item can be one of:`
- **line 40:** `and grouping_element can be one of:`
- **line 49:** `and with_query is:`

### `vi-reference/sql-commands/set-transaction.md`

- **line 13:** `where transaction_mode is one of:`

### `vi-reference/sql-commands/start-transaction.md`

- **line 11:** `where transaction_mode is one of:`

### `vi-reference/sql-commands/vacuum.md`

- **line 11:** `where option can be one of:`
- **line 28:** `and table_and_columns is:`

### `vii-internals/52-system-catalogs/pg-range.md`

- **line 72:** `rngsubopc (plus rngcollation, if the element type is collatable) determines the `

### `vii-internals/52-system-catalogs/pg-statistic.md`

- **line 26:** `pg_statistic should not be readable by the public, since even statistical inform`

### `vii-internals/53-system-views/pg-backend-memory-contexts.md`

- **line 10:** `pg_backend_memory_contexts contains one row for each memory context.`

### `vii-internals/53-system-views/pg-locks.md`

- **line 155:** `pg_locks provides a global view of all locks in the database cluster, not only t`

### `vii-internals/53-system-views/pg-prepared-statements.md`

- **line 11:** `pg_prepared_statements contains one row for each prepared statement.`

### `vii-internals/53-system-views/pg-prepared-xacts.md`

- **line 10:** `pg_prepared_xacts contains one row per prepared transaction.`

### `vii-internals/53-system-views/pg-stats-ext-exprs.md`

- **line 11:** `pg_stats_ext_exprs is also designed to present the information in a more readabl`

### `vii-internals/53-system-views/pg-stats-ext.md`

- **line 11:** `pg_stats_ext is also designed to present the information in a more readable form`

### `vii-internals/53-system-views/pg-stats.md`

- **line 11:** `pg_stats is also designed to present the information in a more readable format t`

### `vii-internals/54-frontend-backend-protocol/streaming-replication-protocol.md`

- **line 404:** `new archive (B)`
- **line 420:** `manifest (B)`
- **line 428:** `archive or manifest data (B)`
- **line 440:** `progress report (B)`

### `vii-internals/65-built-in-index-access-methods/sp-gist-indexes.md`

- **line 784:** `datum is the original datum of spgConfigIn.attType type that was to be inserted `

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-11-dblink-connect-to-other-postgresql-databases.md`

- **line 34:** `dblink_connect(text connstr) returns text dblink_connect(text connname, text con`
- **line 147:** `dblink_connect_u(text connstr) returns text dblink_connect_u(text connname, text`
- **line 170:** `dblink_disconnect() returns text dblink_disconnect(text connname) returns text`
- **line 348:** `dblink_exec(text connname, text sql \[, bool fail_on_error\]) returns text dblin`
- **line 421:** `dblink_open(text cursorname, text sql \[, bool fail_on_error\]) returns text dbl`
- **line 477:** `dblink_fetch(text cursorname, int howmany \[, bool fail_on_error\]) returns seto`
- **line 565:** `dblink_close(text cursorname \[, bool fail_on_error\]) returns text dblink_close`
- **line 619:** `returns the names of all open named dblink connections`
- **line 621:** `dblink_get_connections() returns text\[\]`
- **line 643:** `dblink_error_message(text connname) returns text`
- **line 678:** `dblink_send_query(text connname, text sql) returns int`
- **line 715:** `dblink_is_busy(text connname) returns int`
- **line 746:** `dblink_get_notify() returns setof (notify_name text, be_pid int, extra text) dbl`
- **line 796:** `dblink_get_result(text connname \[, bool fail_on_error\]) returns setof record`
- **line 897:** `dblink_cancel_query(text connname) returns text`
- **line 928:** `returns the positions and field names of a relation\'s primary key fields`
- **line 930:** `dblink_get_pkey(text relname) returns setof dblink_pkey_results`
- **line 980:** `dblink_build_sql_insert(text relname, int2vector primary_key_attnums, integer nu`
- **line 1033:** `dblink_build_sql_delete(text relname, int2vector primary_key_attnums, integer nu`
- **line 1083:** `dblink_build_sql_update(text relname, int2vector primary_key_attnums, integer nu`

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-16-fuzzystrmatch-determine-string-similarities-and-distance.md`

- **line 66:** `text) returns text\[\]`

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-26-pgcrypto-cryptographic-functions.md`

- **line 133:** `gen_salt(type text \[, iter_count integer \]) returns text`
- **line 418:** `pgp_sym_encrypt(data text, psw text \[, options text \]) returns bytea pgp_sym_e`
- **line 424:** `pgp_sym_decrypt(msg bytea, psw text \[, options text \]) returns text pgp_sym_de`
- **line 434:** `pgp_pub_encrypt(data text, key bytea \[, options text \]) returns bytea pgp_pub_`
- **line 442:** `pgp_pub_decrypt(msg bytea, key bytea \[, psw text \[, options text \]\]) returns`
- **line 452:** `pgp_key_id(bytea) returns text`
- **line 470:** `armor(data bytea \[ , keys text\[\], values text\[\] \]) returns text dearmor(da`
- **line 478:** `pgp_armor_headers(data text, key out text, value out text) returns setof record`
- **line 641:** `and *mode* is one of:`
- **line 649:** `and *padding* is one of:`
- **line 664:** `gen_random_bytes(count integer) returns bytea`
- **line 668:** `gen_random_uuid() returns uuid`

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-30-pg-prewarm-preload-relation-data-into-buffer-caches.md`

- **line 15:** `pg_prewarm(regclass, mode text default \'buffer\', fork text default \'main\', f`
- **line 29:** `autoprewarm_start_worker() RETURNS void`
- **line 34:** `autoprewarm_dump_now() RETURNS int8`

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-32-pg-stat-statements-track-statistics-of-sql-planning-and-execution.md`

- **line 474:** `plans and calls aren\'t always expected to match because planning and execution `

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-43-tablefunc-functions-that-return-tables-crosstab-and-others.md`

- **line 99:** `crosstab(text sql) crosstab(text sql, int N)`

### `viii-appendixes/j-documentation/j-5-documentation-authoring.md`

- **line 15:** `nXML Mode, which ships with Emacs, is the most common mode for editing XML docum`

## AMBIGUOUS (40)

_Multiple XML hits — skipped by script, review manually_

### `i-tutorial/advanced-features/inheritance.md`

- **line 58:** `which returns:`
  - _2 filtered hits_

### `ii-the-sql-language/07-queries/table-expressions.md`

- **line 735:** `is equivalent to`
  - _5 filtered hits_
- **line 754:** `is equivalent to`
  - _5 filtered hits_
- **line 767:** `is equivalent to`
  - _5 filtered hits_
- **line 784:** `is equivalent to`
  - _2 filtered hits_
- **line 795:** `is equivalent to`
  - _2 filtered hits_
- **line 814:** `is equivalent to`
  - _2 filtered hits_

### `ii-the-sql-language/07-queries/values-lists.md`

- **line 17:** `will return a table of two columns and three rows.`
  - _2 filtered hits_

### `ii-the-sql-language/08-data-types/xml-type.md`

- **line 30:** `can also be used.`
  - _2 hits, no code ctx_

### `ii-the-sql-language/09-functions-and-operators/event-trigger-functions.md`

- **line 18:** `setof record`
  - _52 hits, no code ctx_
- **line 143:** `setof record`
  - _52 hits, no code ctx_

### `ii-the-sql-language/09-functions-and-operators/row-and-array-comparisons.md`

- **line 63:** `array expression`
  - _5 hits, no code ctx_
- **line 73:** `array expression`
  - _5 hits, no code ctx_
- **line 97:** `array expression`
  - _5 hits, no code ctx_

### `ii-the-sql-language/09-functions-and-operators/statistics-information-functions.md`

- **line 20:** `setof record`
  - _52 hits, no code ctx_

### `ii-the-sql-language/09-functions-and-operators/xml-functions.md`

- **line 725:** `setof record`
  - _52 hits, no code ctx_

### `ii-the-sql-language/12-full-text-search/additional-features.md`

- **line 295:** `setof record`
  - _52 hits_

### `ii-the-sql-language/12-full-text-search/testing-and-debugging-text-search.md`

- **line 182:** `setof record`
  - _52 hits, no code ctx_
- **line 210:** `setof record`
  - _52 hits_
- **line 252:** `setof record`
  - _52 hits, no code ctx_
- **line 280:** `setof record`
  - _52 hits_

### `iii-server-administration/22-managing-databases/creating-a-database.md`

- **line 44:** `from the shell.`
  - _3 hits, no code ctx_

### `iii-server-administration/22-managing-databases/template-databases.md`

- **line 32:** `from the shell.`
  - _3 hits, no code ctx_

### `iii-server-administration/23-localization/collation-support.md`

- **line 70:** `or equivalently`
  - _6 hits_

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/embedded-sql-commands.md`

- **line 93:** `host variable`
  - _73 hits_

### `v-server-programming/36-extending-sql/interfacing-extensions-to-indexes.md`

- **line 919:** `finds the ten places closest to a given target point.`
  - _2 hits_

### `v-server-programming/37-triggers/writing-trigger-functions-in-c.md`

- **line 19:** `which expands to:`
  - _2 filtered hits_
- **line 43:** `where the members are defined as follows:`
  - _2 hits, no code ctx_

### `v-server-programming/38-event-triggers/writing-event-trigger-functions-in-c.md`

- **line 19:** `which expands to:`
  - _2 filtered hits_
- **line 36:** `where the members are defined as follows:`
  - _2 hits, no code ctx_

### `v-server-programming/39-the-rule-system/rules-on-insert-update-and-delete.md`

- **line 38:** `in mind.`
  - _4 hits, no code ctx_

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 785:** `can be used with`
  - _34 hits, no code ctx_
- **line 819:** `execute a statement prepared by`
  - _3 hits, no code ctx_
- **line 892:** `execute a statement prepared by`
  - _3 hits, no code ctx_
- **line 970:** `execute a statement prepared by`
  - _3 hits, no code ctx_

### `v-server-programming/45-server-programming-interface/interface-support-functions.md`

- **line 239:** `of the specified column`
  - _8 hits, no code ctx_

### `v-server-programming/45-server-programming-interface/transaction-management.md`

- **line 24:** `commit the current transaction`
  - _4 hits, no code ctx_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-12-dict-int-example-full-text-search-dictionary-for-integers.md`

- **line 31:** `or create new dictionaries based on the template.`
  - _3 hits_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-13-dict-xsyn-example-synonym-full-text-search-dictionary.md`

- **line 43:** `or create new dictionaries based on the template.`
  - _3 hits_

### `viii-appendixes/g-additional-supplied-programs/g-1-client-applications.md`

- **line 24:** `data directory`
  - _139 hits, no code ctx_

## ALREADY (31)

_Duplicate insert point within file — covered by sibling orphan_

### `i-tutorial/the-sql-language/aggregate-functions.md`

- **line 49:** `which gives us one output row per city.`
  - _para already handled_

### `ii-the-sql-language/04-sql-syntax/lexical-structure.md`

- **line 118:** `is equivalent to:`
  - _para already handled_

### `ii-the-sql-language/05-data-definition/inheritance.md`

- **line 77:** `which returns:`
  - _para already handled_

### `ii-the-sql-language/07-queries/table-expressions.md`

- **line 257:** `is valid SQL, but:`
  - _para already handled_

### `ii-the-sql-language/07-queries/with-queries-common-table-expressions.md`

- **line 395:** `the outer `SELECT` would return the original prices before the action of the `UP`
  - _para already handled_

### `ii-the-sql-language/08-data-types/arrays.md`

- **line 227:** `or using the `ARRAY` expression syntax:`
  - _para already handled_

### `ii-the-sql-language/08-data-types/composite-types.md`

- **line 171:** `then, according to the SQL standard, we should get the contents of the table exp`
  - _para already handled_

### `ii-the-sql-language/08-data-types/date-time-types.md`

- **line 412:** `are valid values, which follow the ISO 8601 standard. In addition, the common fo`
  - _para already handled_

### `ii-the-sql-language/08-data-types/numeric-types.md`

- **line 112:** `will round values to the nearest thousand and can store values between -99000 an`
  - _para already handled_

### `ii-the-sql-language/11-indexes/index-only-scans-and-covering-indexes.md`

- **line 54:** `the traditional approach to speeding up such queries would be to create an index`
  - _para already handled_

### `ii-the-sql-language/11-indexes/indexes-and-collations.md`

- **line 25:** `could use the index, because the comparison will by default use the collation of`
  - _para already handled_

### `ii-the-sql-language/13-concurrency-control/transaction-isolation.md`

- **line 255:** `and then inserts the result (30) as the value in a new row with class`= 2`.`
  - _para already handled_

### `ii-the-sql-language/14-performance-tips/statistics-used-by-the-planner.md`

- **line 150:** `the planner will disregard the city clause as not changing the selectivity, whic`
  - _para already handled_

### `iii-server-administration/21-database-roles/role-membership.md`

- **line 35:** `the session would have use of only those privileges granted to `admin`, and not `
  - _para already handled_

### `iii-server-administration/23-localization/collation-support.md`

- **line 85:** `the ordering will be done according to `de_DE` rules.`
  - _para already handled_

### `iii-server-administration/31-regression-tests/running-the-tests.md`

- **line 20:** `in the top-level directory. (Or you can change to `src/test/regress` and run the`
  - _para already handled_

### `iv-client-interfaces/34-ecpg-embedded-sql-in-c/using-host-variables.md`

- **line 37:** `and ends with:`
  - _insert point 37 used_

### `v-server-programming/36-extending-sql/c-language-functions.md`

- **line 654:** `to get a TupleDesc for the row type of a named relation, and:`
  - _para already handled_
- **line 666:** `if you plan to work with Datums, or:`
  - _para already handled_

### `v-server-programming/39-the-rule-system/rules-on-insert-update-and-delete.md`

- **line 112:** `and we look at the log table:`
  - _insert point 114 used_
- **line 133:** `and the action:`
  - _insert point 114 used_
- **line 221:** `no log entry would get written.`
  - _para already handled_

### `v-server-programming/39-the-rule-system/rules-versus-triggers.md`

- **line 54:** `the table `computer` is scanned by index (fast), and the command issued by the t`
  - _insert point 54 used_
- **line 80:** `with the plan`
  - _para already handled_

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 117:** `will retrieve at most 5 rows from the table.`
  - _para already handled_

### `vi-reference/client-apps/psql.md`

- **line 1037:** `will result in the three SQL commands being individually sent to the server, wit`
  - _para already handled_

### `vi-reference/server-apps/pg-archivecleanup.md`

- **line 23:** `where *archivelocation* is the directory from which WAL segment files should be `
  - _insert point 23 used_

### `vii-internals/54-frontend-backend-protocol/message-flow.md`

- **line 191:** `then the first `INSERT` is committed by the explicit `COMMIT` command.`
  - _insert point 189 used_
- **line 215:** `in a single Query message, the session will be left inside a failed regular tran`
  - _insert point 189 used_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/index.md`

- **line 19:** `in the `contrib` directory of a configured source tree; or to build and install `
  - _para already handled_
- **line 24:** `before installation or`
  - _para already handled_

## OTHER (141)

_Miscellaneous skip_

### `i-tutorial/getting-started/index.md`

- **line 66:** `then PostgreSQL was not installed properly.`
  - _stale lineno_
- **line 87:** `where your own login name is mentioned.`
  - _stale lineno_
- **line 188:** `and `psql` will quit and return you to your command shell. (For more internal co`
  - _stale lineno_

### `ii-the-sql-language/04-sql-syntax/lexical-structure.md`

- **line 510:** `the `OPERATOR` construct is taken to have the default precedence shown in Operat`
  - _stale lineno_

### `ii-the-sql-language/04-sql-syntax/value-expressions.md`

- **line 182:** `not this:`
  - _text not in file_
- **line 212:** `which obtains the 50th percentile, or median, value of the income column from ta`
  - _text not in file_
- **line 341:** `and overriding the collation of a function or operator call that has locale-sens`
  - _text not in file_
- **line 355:** `because it attempts to apply a collation to the result of the `>` operator, whic`
  - _text not in file_
- **line 525:** `then `somefunc()` would (probably) not be called at all.`
  - _text not in file_
- **line 554:** `is likely to result in a division-by-zero failure due to the planner trying to s`
  - _text not in file_

### `ii-the-sql-language/05-data-definition/constraints.md`

- **line 78:** `or even:`
  - _text not in file_
- **line 178:** `and then insert the `NOT` key word where desired.`
  - _text not in file_
- **line 195:** `when written as a column constraint, and:`
  - _text not in file_
- **line 204:** `when written as a table constraint.`
  - _text not in file_
- **line 324:** `because in absence of a column list the primary key of the referenced table is u`
  - _text not in file_

### `iii-server-administration/17-installation-from-source-code/post-installation-setup.md`

- **line 66:** `man documentation, you need to add lines like the following to a shell start-up `
  - _bad insert point_

### `iii-server-administration/25-backup-and-restore/sql-dump.md`

- **line 14:** `pg_dump is a regular PostgreSQL client application (albeit a particularly clever`
  - _nothing dropped_
- **line 68:** `pg_dump dumps only a single database at a time, and it does not dump information`
  - _nothing dropped_

### `iii-server-administration/29-logical-replication/upgrade.md`

- **line 12:** `pg_upgrade attempts to migrate logical slots.`
  - _nothing dropped_

### `iv-client-interfaces/32-libpq-c-library/index.md`

- **line 8:** `libpq is also the underlying engine for several other PostgreSQL application int`
  - _nothing dropped_

### `iv-client-interfaces/32-libpq-c-library/oauth-support.md`

- **line 8:** `libpq implements support for the OAuth v2 Device Authorization client flow, docu`
  - _nothing dropped_

### `iv-client-interfaces/32-libpq-c-library/pipeline-mode.md`

- **line 8:** `libpq pipeline mode allows applications to send a query without having to read t`
  - _nothing dropped_
- **line 59:** `libpq does not provide any information to the application about the query curren`
  - _nothing dropped_

### `iv-client-interfaces/32-libpq-c-library/ssl-support.md`

- **line 11:** `libpq reads the system-wide OpenSSL configuration file.`
  - _nothing dropped_

### `v-server-programming/36-extending-sql/query-language-sql-functions.md`

- **line 616:** `is almost equivalent to`
  - _text not in file_
- **line 635:** `the set-returning functions `srf2`, `srf3`, and `srf5` would be run in lockstep `
  - _text not in file_
- **line 654:** `could become`
  - _text not in file_
- **line 803:** `will depend on the database\'s default collation.`
  - _text not in file_

### `v-server-programming/38-event-triggers/writing-event-trigger-functions-in-c.md`

- **line 26:** `struct EventTriggerData is defined in `commands/event_trigger.h`:`
  - _bad insert point_

### `v-server-programming/39-the-rule-system/rules-on-insert-update-and-delete.md`

- **line 514:** `while omitting the extra range table entry would result in a`
  - _pattern_a_mismatch_
- **line 524:** `which produces exactly the same entries in the log table.`
  - _pattern_a_mismatch_

### `v-server-programming/45-server-programming-interface/interface-functions.md`

- **line 88:** `execute a command`
  - _pattern_a_mismatch_
- **line 781:** `if a statement prepared by`
  - _pattern_a_mismatch_
- **line 1395:** `pointer to the portal with the specified name, or `NULL` if none was found`
  - _nothing dropped_

### `v-server-programming/45-server-programming-interface/memory-management.md`

- **line 55:** `pointer to new storage space of the specified size`
  - _nothing dropped_
- **line 95:** `pointer to new storage space of specified size with the contents copied from the`
  - _nothing dropped_
- **line 159:** `the copied row, or `NULL` on error (see `SPI_result` for an error indication)`
  - _nothing dropped_
- **line 275:** `new row with modifications, allocated in the upper executor context, or `NULL` o`
  - _nothing dropped_

### `v-server-programming/46-background-worker-processes.md`

- **line 74:** `bgw_extra can contain extra data to be passed to the background worker.`
  - _nothing dropped_

### `vi-reference/client-apps/clusterdb.md`

- **line 32:** `clusterdb is a utility for reclustering tables in a PostgreSQL database.`
  - _nothing dropped_
- **line 41:** `clusterdb accepts the following command-line arguments:`
  - _nothing dropped_
- **line 70:** `clusterdb also accepts the following command-line arguments for connection param`
  - _nothing dropped_

### `vi-reference/client-apps/createdb.md`

- **line 20:** `createdb creates a new PostgreSQL database.`
  - _nothing dropped_
- **line 25:** `createdb is a wrapper around the SQL command [`CREATE DATABASE`](#sql-createdata`
  - _nothing dropped_
- **line 30:** `createdb accepts the following command-line arguments:`
  - _nothing dropped_
- **line 88:** `createdb also accepts the following command-line arguments for connection parame`
  - _nothing dropped_

### `vi-reference/client-apps/createuser.md`

- **line 17:** `createuser creates a new PostgreSQL user (or more precisely, a role).`
  - _nothing dropped_
- **line 23:** `createuser is a wrapper around the SQL command [`CREATE ROLE`](#sql-createrole).`
  - _nothing dropped_
- **line 28:** `createuser accepts the following command-line arguments:`
  - _nothing dropped_
- **line 111:** `createuser also accepts the following command-line arguments for connection para`
  - _nothing dropped_

### `vi-reference/client-apps/dropdb.md`

- **line 17:** `dropdb destroys an existing PostgreSQL database.`
  - _nothing dropped_
- **line 20:** `dropdb is a wrapper around the SQL command [`DROP DATABASE`](#sql-dropdatabase).`
  - _nothing dropped_
- **line 25:** `dropdb accepts the following command-line arguments:`
  - _nothing dropped_
- **line 51:** `dropdb also accepts the following command-line arguments for connection paramete`
  - _nothing dropped_

### `vi-reference/client-apps/dropuser.md`

- **line 17:** `dropuser removes an existing PostgreSQL user.`
  - _nothing dropped_
- **line 25:** `dropuser accepts the following command-line arguments:`
  - _nothing dropped_
- **line 48:** `dropuser also accepts the following command-line arguments for connection parame`
  - _nothing dropped_

### `vi-reference/client-apps/pg-amcheck.md`

- **line 215:** `pg_amcheck is designed to work with PostgreSQL 14.0 and later.`
  - _nothing dropped_

### `vi-reference/client-apps/pg-basebackup.md`

- **line 15:** `pg_basebackup is used to take a base backup of a running PostgreSQL database clu`
  - _nothing dropped_
- **line 18:** `pg_basebackup can take a full or incremental base backup of the database.`
  - _nothing dropped_
- **line 36:** `pg_basebackup can make a base backup from not only a primary server but also a s`
  - _nothing dropped_
- **line 298:** `pg_basebackup works with servers of the same or older major version, down to 9.1`
  - _nothing dropped_
- **line 301:** `pg_basebackup will preserve group permissions for data files if group permission`
  - _nothing dropped_

### `vi-reference/client-apps/pg-combinebackup.md`

- **line 16:** `pg_combinebackup is used to reconstruct a synthetic full backup from an [increme`
  - _nothing dropped_
- **line 22:** `pg_combinebackup will attempt to verify that the backups you specify form a lega`
  - _nothing dropped_

### `vi-reference/client-apps/pg-dump.md`

- **line 19:** `pg_dump is a utility for exporting a PostgreSQL database.`
  - _nothing dropped_
- **line 24:** `pg_dump only dumps a single database.`
  - _nothing dropped_
- **line 444:** `pg_dump internally executes `SELECT` statements.`
  - _nothing dropped_

### `vi-reference/client-apps/pg-dumpall.md`

- **line 28:** `pg_dumpall needs to connect several times to the PostgreSQL server (once per dat`
  - _nothing dropped_
- **line 259:** `pg_dumpall requires all needed tablespace directories to exist before the restor`
  - _nothing dropped_

### `vi-reference/client-apps/pg-isready.md`

- **line 18:** `pg_isready is a utility for checking the connection status of a PostgreSQL datab`
  - _nothing dropped_
- **line 54:** `pg_isready returns `0` to the shell if the server is accepting connections norma`
  - _nothing dropped_

### `vi-reference/client-apps/pg-receivewal.md`

- **line 15:** `pg_receivewal is used to stream the write-ahead log from a running PostgreSQL cl`
  - _nothing dropped_
- **line 132:** `pg_receivewal can perform one of the two following actions in order to control p`
  - _nothing dropped_
- **line 156:** `pg_receivewal will exit with status 0 when terminated by the `SIGINT` or `SIGTER`
  - _nothing dropped_
- **line 178:** `pg_receivewal will preserve group permissions on the received WAL files if group`
  - _nothing dropped_

### `vi-reference/client-apps/pg-recvlogical.md`

- **line 154:** `pg_recvlogical will exit with status 0 when terminated by the `SIGINT` or `SIGTE`
  - _nothing dropped_
- **line 166:** `pg_recvlogical will preserve group permissions on the received WAL files if grou`
  - _nothing dropped_

### `vi-reference/client-apps/pg-restore.md`

- **line 25:** `pg_restore can operate in two modes.`
  - _nothing dropped_
- **line 42:** `pg_restore accepts the following command line arguments.`
  - _nothing dropped_
- **line 267:** `pg_restore also accepts the following command line arguments for connection para`
  - _nothing dropped_

### `vi-reference/client-apps/pg-verifybackup.md`

- **line 51:** `pg_verifybackup accepts the following command-line arguments:`
  - _nothing dropped_

### `vi-reference/client-apps/pgbench.md`

- **line 20:** `pgbench is a simple program for running benchmark tests on PostgreSQL.`
  - _nothing dropped_
- **line 83:** `pgbench accepts the following command-line initialization arguments:`
  - _nothing dropped_
- **line 161:** `pgbench accepts the following command-line benchmarking arguments:`
  - _nothing dropped_
- **line 293:** `pgbench also accepts the following common command-line arguments for connection `
  - _nothing dropped_
- **line 341:** `pgbench executes test scripts chosen randomly from a specified list.`
  - _nothing dropped_
- **line 371:** `pgbench has support for running custom benchmark scenarios by replacing the defa`
  - _nothing dropped_

### `vi-reference/client-apps/psql.md`

- **line 173:** `psql returns 0 to the shell if it finished normally, 1 if a fatal error of its o`
  - _nothing dropped_
- **line 179:** `psql is a regular PostgreSQL client application.`
  - _nothing dropped_
- **line 1083:** `psql provides variable substitution features similar to common Unix command shel`
  - _nothing dropped_
- **line 1397:** `psql uses the Readline or libedit library, if available, for convenient line edi`
  - _nothing dropped_

### `vi-reference/client-apps/reindexdb.md`

- **line 61:** `reindexdb is a utility for rebuilding indexes in a PostgreSQL database.`
  - _nothing dropped_
- **line 68:** `reindexdb accepts the following command-line arguments:`
  - _nothing dropped_
- **line 89:** `reindexdb will open *njobs* connections to the database, so make sure your [max_`
  - _nothing dropped_
- **line 121:** `reindexdb also accepts the following command-line arguments for connection param`
  - _nothing dropped_

### `vi-reference/client-apps/vacuumdb.md`

- **line 71:** `vacuumdb is a utility for cleaning a PostgreSQL database. vacuumdb will also gen`
  - _nothing dropped_
- **line 78:** `vacuumdb accepts the following command-line arguments:`
  - _nothing dropped_
- **line 108:** `vacuumdb will open *njobs* connections to the database, so make sure your [max_c`
  - _nothing dropped_
- **line 189:** `vacuumdb also accepts the following command-line arguments for connection parame`
  - _nothing dropped_

### `vi-reference/server-apps/pg-archivecleanup.md`

- **line 40:** `pg_archivecleanup assumes that *archivelocation* is a directory readable and wri`
  - _nothing dropped_
- **line 44:** `pg_archivecleanup accepts the following command-line arguments:`
  - _nothing dropped_
- **line 74:** `pg_archivecleanup is designed to work with PostgreSQL 8.0 and later when used as`
  - _nothing dropped_
- **line 76:** `pg_archivecleanup is written in C and has an easy-to-modify source code, with sp`
  - _nothing dropped_

### `vi-reference/server-apps/pg-checksums.md`

- **line 23:** `pg_checksums checks, enables or disables data checksums in a PostgreSQL cluster.`
  - _nothing dropped_

### `vi-reference/server-apps/pg-createsubscriber.md`

- **line 31:** `pg_createsubscriber creates a new logical replica from a physical standby server`
  - _nothing dropped_
- **line 40:** `pg_createsubscriber targets large database systems because in logical replicatio`
  - _nothing dropped_
- **line 47:** `pg_createsubscriber accepts the following command-line arguments:`
  - _nothing dropped_
- **line 146:** `pg_createsubscriber usually starts the target server with different connection s`
  - _nothing dropped_

### `vi-reference/server-apps/pg-ctl.md`

- **line 99:** `pg_ctl is a utility for initializing a PostgreSQL database cluster, starting, st`
  - _nothing dropped_

### `vi-reference/server-apps/pg-rewind.md`

- **line 24:** `pg_rewind is a tool for synchronizing a PostgreSQL cluster with another copy of `
  - _nothing dropped_
- **line 62:** `pg_rewind accepts the following command-line arguments:`
  - _nothing dropped_

### `vi-reference/server-apps/pg-upgrade.md`

- **line 28:** `pg_upgrade does its best to make sure the old and new clusters are binary-compat`
  - _nothing dropped_
- **line 31:** `pg_upgrade supports upgrades from 9.2.X and later to the current major release o`
  - _nothing dropped_
- **line 39:** `pg_upgrade accepts the following command-line arguments:`
  - _nothing dropped_
- **line 321:** `pg_upgrade launches short-lived postmasters in the old and new data directories.`
  - _nothing dropped_
- **line 332:** `pg_upgrade does not support upgrading of databases containing table columns usin`
  - _nothing dropped_

### `vi-reference/server-apps/pg-walsummary.md`

- **line 16:** `pg_walsummary is used to print the contents of WAL summary files.`
  - _nothing dropped_

### `vi-reference/sql-commands/create-procedure.md`

- **line 142:** `and call like this:`
  - _no intro in para_

### `vii-internals/52-system-catalogs/pg-statistic.md`

- **line 16:** `pg_statistic also stores statistical data about the values of index expressions.`
  - _nothing dropped_

### `vii-internals/53-system-views/pg-locks.md`

- **line 11:** `pg_locks contains one row per active lockable object, requested lock mode, and r`
  - _nothing dropped_
- **line 143:** `granted is true in a row representing a lock held by the indicated process. Fals`
  - _nothing dropped_

### `vii-internals/60-writing-a-custom-scan-provider/creating-custom-scan-paths.md`

- **line 29:** `path must be initialized as for any other path, including the row-count estimate`
  - _nothing dropped_

### `vii-internals/60-writing-a-custom-scan-provider/creating-custom-scan-plans.md`

- **line 22:** `scan must be initialized as for any other scan, including estimated costs, targe`
  - _nothing dropped_

### `vii-internals/60-writing-a-custom-scan-provider/executing-custom-scans.md`

- **line 17:** `ss is initialized as for any other scan state, except that if the scan is for a `
  - _nothing dropped_

### `vii-internals/65-built-in-index-access-methods/brin-indexes.md`

- **line 2128:** `bloom operator classes accept these parameters:`
  - _nothing dropped_
- **line 2139:** `minmax-multi operator classes accept these parameters:`
  - _nothing dropped_

### `vii-internals/65-built-in-index-access-methods/sp-gist-indexes.md`

- **line 717:** `leafType should match the index storage type defined by the operator class\'s op`
  - _nothing dropped_
- **line 873:** `nNodes must be set to the number of child nodes that need to be visited by the s`
  - _nothing dropped_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-10-cube-a-multi-dimensional-cube-data-type.md`

- **line 352:** `does not contradict common sense, neither does the intersection:`
  - _nothing dropped_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-23-pageinspect-low-level-inspection-of-database-pages.md`

- **line 195:** `htid shows a heap TID for the tuple, regardless of the underlying tuple represen`
  - _nothing dropped_

### `viii-appendixes/f-additional-supplied-modules-and-extensions/f-50-xml2-xpath-querying-and-xslt-functionality.md`

- **line 160:** `so those parameters can be *anything* valid in those particular locations. The r`
  - _nothing dropped_

### `viii-appendixes/g-additional-supplied-programs/g-1-client-applications.md`

- **line 32:** `oid2name is a utility program that helps administrators to examine the file stru`
  - _nothing dropped_
- **line 39:** `oid2name connects to a target database and extracts OID, filenode, and/or table `
  - _nothing dropped_
- **line 44:** `oid2name accepts the following command-line arguments:`
  - _nothing dropped_
- **line 79:** `oid2name also accepts the following command-line arguments for connection parame`
  - _nothing dropped_
- **line 124:** `oid2name requires a running database server with non-corrupt system catalogs.`
  - _nothing dropped_
- **line 272:** `vacuumlo is a simple utility program that will remove any "orphaned" large objec`
  - _nothing dropped_
- **line 281:** `vacuumlo accepts the following command-line arguments:`
  - _nothing dropped_
- **line 303:** `vacuumlo also accepts the following command-line arguments for connection parame`
  - _nothing dropped_
- **line 340:** `vacuumlo works by the following method: First, vacuumlo builds a temporary table`
  - _nothing dropped_

