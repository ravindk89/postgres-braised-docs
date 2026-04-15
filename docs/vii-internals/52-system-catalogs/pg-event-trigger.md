---
title: "52.21. pg_event_trigger"
id: catalog-pg-event-trigger
---

## pg_event_trigger

The catalog pg_event_trigger stores event triggers.
See [Event Triggers](#event-triggers) for more information.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evtname `name`

   Trigger name (must be unique)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evtevent `name`

   Identifies the event for which this trigger fires
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evtowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the event trigger
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evtfoid `oid` (references [pg_proc](#catalog-pg-proc).oid)

   The function to be called
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evtenabled `char`

   Controls in which [session_replication_role (enum)
      
       session_replication_role configuration parameter](braised:ref/runtime-config-client#session-replication-role-enum-session-replication-role-configuration-parameter) modes the event trigger fires. `O` = trigger fires in "origin" and "local" modes, `D` = trigger is disabled, `R` = trigger fires in "replica" mode, `A` = trigger fires always.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   evttags `text[]`

   Command tags for which this trigger will fire. If NULL, the firing of this trigger is not restricted on the basis of the command tag.
  :::{/cell}
  :::{/row}
:::{/table}

: pg_event_trigger Columns
