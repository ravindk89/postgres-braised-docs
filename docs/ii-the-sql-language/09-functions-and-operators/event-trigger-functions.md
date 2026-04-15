---
title: "9.30. Event Trigger Functions"
id: functions-event-triggers
---

## Event Trigger Functions

PostgreSQL provides these helper functions to retrieve information from event triggers.

For more information about event triggers, see [Event Triggers](#event-triggers).

### Capturing Changes at Command End

pg_event_trigger_ddl_commands

()

setof record

`pg_event_trigger_ddl_commands` returns a list of DDL commands executed by each user action, when invoked in a function attached to a `ddl_command_end` event trigger.
If called in any other context, an error is raised. `pg_event_trigger_ddl_commands` returns one row for each base command executed; some commands that are a single SQL sentence may return more than one row.
This function returns the following columns:

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Type
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `classid`
  :::{/cell}
  :::{.cell}
  `oid`
  :::{/cell}
  :::{.cell}
  OID of catalog the object belongs in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `objid`
  :::{/cell}
  :::{.cell}
  `oid`
  :::{/cell}
  :::{.cell}
  OID of the object itself
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `objsubid`
  :::{/cell}
  :::{.cell}
  `integer`
  :::{/cell}
  :::{.cell}
  Sub-object ID (e.g., attribute number for a column)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `command_tag`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Command tag
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object_type`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Type of the object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `schema_name`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Name of the schema the object belongs in, if any; otherwise `NULL`. No quoting is applied.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object_identity`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Text rendering of the object identity, schema-qualified. Each identifier included in the identity is quoted if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `in_extension`
  :::{/cell}
  :::{.cell}
  `boolean`
  :::{/cell}
  :::{.cell}
  True if the command is part of an extension script
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `command`
  :::{/cell}
  :::{.cell}
  `pg_ddl_command`
  :::{/cell}
  :::{.cell}
  A complete representation of the command, in internal format. This cannot be output directly, but it can be passed to other functions to obtain different pieces of information about the command.
  :::{/cell}
  :::{/row}
:::{/table}

### Processing Objects Dropped by a DDL Command

pg_event_trigger_dropped_objects

()

setof record

`pg_event_trigger_dropped_objects` returns a list of all objects dropped by the command in whose `sql_drop` event it is called. If called in any other context, an error is raised. This function returns the following columns:

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Name
  :::{/cell}
  :::{.cell}
  Type
  :::{/cell}
  :::{.cell}
  Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `classid`
  :::{/cell}
  :::{.cell}
  `oid`
  :::{/cell}
  :::{.cell}
  OID of catalog the object belonged in
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `objid`
  :::{/cell}
  :::{.cell}
  `oid`
  :::{/cell}
  :::{.cell}
  OID of the object itself
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `objsubid`
  :::{/cell}
  :::{.cell}
  `integer`
  :::{/cell}
  :::{.cell}
  Sub-object ID (e.g., attribute number for a column)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `original`
  :::{/cell}
  :::{.cell}
  `boolean`
  :::{/cell}
  :::{.cell}
  True if this was one of the root object(s) of the deletion
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `normal`
  :::{/cell}
  :::{.cell}
  `boolean`
  :::{/cell}
  :::{.cell}
  True if there was a normal dependency relationship in the dependency graph leading to this object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `is_temporary`
  :::{/cell}
  :::{.cell}
  `boolean`
  :::{/cell}
  :::{.cell}
  True if this was a temporary object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object_type`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Type of the object
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `schema_name`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Name of the schema the object belonged in, if any; otherwise `NULL`. No quoting is applied.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object_name`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Name of the object, if the combination of schema and name can be used as a unique identifier for the object; otherwise `NULL`. No quoting is applied, and name is never schema-qualified.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `object_identity`
  :::{/cell}
  :::{.cell}
  `text`
  :::{/cell}
  :::{.cell}
  Text rendering of the object identity, schema-qualified. Each identifier included in the identity is quoted if necessary.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `address_names`
  :::{/cell}
  :::{.cell}
  `text[]`
  :::{/cell}
  :::{.cell}
  An array that, together with `object_type` and `address_args`, can be used by the `pg_get_object_address` function to recreate the object address in a remote server containing an identically named object of the same kind.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  `address_args`
  :::{/cell}
  :::{.cell}
  `text[]`
  :::{/cell}
  :::{.cell}
  Complement for `address_names`
  :::{/cell}
  :::{/row}
:::{/table}

The `pg_event_trigger_dropped_objects` function can be used in an event trigger like this:

    CREATE FUNCTION test_event_trigger_for_drops()
            RETURNS event_trigger LANGUAGE plpgsql AS $$
    DECLARE
        obj record;
    BEGIN
        FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
        LOOP
            RAISE NOTICE '% dropped object: % %.% %',
                         tg_tag,
                         obj.object_type,
                         obj.schema_name,
                         obj.object_name,
                         obj.object_identity;
        END LOOP;
    END;
    $$;
    CREATE EVENT TRIGGER test_event_trigger_for_drops
       ON sql_drop
       EXECUTE FUNCTION test_event_trigger_for_drops();

### Handling a Table Rewrite Event

The functions shown in [Table Rewrite Information Functions](#functions-event-trigger-table-rewrite) provide information about a table for which a `table_rewrite` event has just been called. If called in any other context, an error is raised.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_event_trigger_table_rewrite_oid` () oid

   Returns the OID of the table about to be rewritten.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `pg_event_trigger_table_rewrite_reason` () integer

   Returns a code explaining the reason(s) for rewriting. The value is a bitmap built from the following values: `1` (the table has changed its persistence), `2` (default value of a column has changed), `4` (a column has a new data type) and `8` (the table access method has changed).
  :::{/cell}
  :::{/row}
:::{/table}

: Table Rewrite Information Functions

These functions can be used in an event trigger like this:

    CREATE FUNCTION test_event_trigger_table_rewrite_oid()
     RETURNS event_trigger
     LANGUAGE plpgsql AS
    $$
    BEGIN
      RAISE NOTICE 'rewriting table % for reason %',
                    pg_event_trigger_table_rewrite_oid()::regclass,
                    pg_event_trigger_table_rewrite_reason();
    END;
    $$;

    CREATE EVENT TRIGGER test_table_rewrite_oid
                      ON table_rewrite
       EXECUTE FUNCTION test_event_trigger_table_rewrite_oid();
