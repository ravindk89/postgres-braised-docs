---
title: "18.12. Registering Event Log on Windows"
id: event-log-registration
---

## Registering Event Log on `Windows`

To register a `Windows` event log library with the operating system, issue this command:

    regsvr32 pgsql_library_directory/pgevent.dll

This creates registry entries used by the event viewer, under the default event source named `PostgreSQL`.

To specify a different event source name (see [event_source (string)
      
       event_source configuration parameter](braised:ref/runtime-config-logging#event-source-string-event-source-configuration-parameter)), use the `/n` and `/i` options:

    regsvr32 /n /i:event_source_name pgsql_library_directory/pgevent.dll

To unregister the event log library from the operating system, issue this command:

    regsvr32 /u [/i:event_source_name] pgsql_library_directory/pgevent.dll

:::{.callout type="note"}
To enable event logging in the database server, modify [log_destination (string)
      
       log_destination configuration parameter](braised:ref/runtime-config-logging#log-destination-string-log-destination-configuration-parameter) to include `eventlog` in `postgresql.conf`.
:::
