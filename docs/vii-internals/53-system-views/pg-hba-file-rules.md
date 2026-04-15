---
title: "53.10. pg_hba_file_rules"
id: view-pg-hba-file-rules
---

## pg_hba_file_rules

The view pg_hba_file_rules provides a summary of the contents of the client authentication configuration file, [`pg_hba.conf`](#auth-pg-hba-conf).
A row appears in this view for each non-empty, non-comment line in the file, with annotations indicating whether the rule could be applied successfully.

This view can be helpful for checking whether planned changes in the authentication configuration file will work, or for diagnosing a previous failure.
Note that this view reports on the *current* contents of the file, not on what was last loaded by the server.

By default, the pg_hba_file_rules view can be read only by superusers.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   rule_number `int4`

   Number of this rule, if valid, otherwise `NULL`. This indicates the order in which each rule is considered until a match is found during authentication.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   file_name `text`

   Name of the file containing this rule
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   line_number `int4`

   Line number of this rule in `file_name`
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   type `text`

   Type of connection
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   database `text[]`

   List of database name(s) to which this rule applies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   user_name `text[]`

   List of user and group name(s) to which this rule applies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   address `text`

   Host name or IP address, or one of `all`, `samehost`, or `samenet`, or null for local connections
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   netmask `text`

   IP address mask, or null if not applicable
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   auth_method `text`

   Authentication method
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   options `text[]`

   Options specified for authentication method, if any
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   error `text`

   If not null, an error message indicating why this line could not be processed
  :::{/cell}
  :::{/row}
:::{/table}

: pg_hba_file_rules Columns

Usually, a row reflecting an incorrect entry will have values for only the line_number and error fields.

See [Client Authentication](#client-authentication) for more information about client authentication configuration.
