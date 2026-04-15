---
title: "52.60. pg_ts_config_map"
id: catalog-pg-ts-config-map
---

## pg_ts_config_map

The pg_ts_config_map catalog contains entries showing which text search dictionaries should be consulted, and in what order, for each output token type of each text search configuration\'s parser.

PostgreSQL\'s text search features are described at length in [Full Text Search](#full-text-search).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Column Type

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   mapcfg `oid` (references [pg_ts_config](#catalog-pg-ts-config).oid)

   The OID of the [pg_ts_config](#catalog-pg-ts-config) entry owning this map entry
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   maptokentype `int4`

   A token type emitted by the configuration\'s parser
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   mapseqno `int4`

   Order in which to consult this entry (lower mapseqnos first)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   mapdict `oid` (references [pg_ts_dict](#catalog-pg-ts-dict).oid)

   The OID of the text search dictionary to consult
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ts_config_map Columns
