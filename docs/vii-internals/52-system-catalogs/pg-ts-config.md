---
title: "52.59. pg_ts_config"
id: catalog-pg-ts-config
---

## pg_ts_config

The pg_ts_config catalog contains entries representing text search configurations.
A configuration specifies a particular text search parser and a list of dictionaries to use for each of the parser\'s output token types.
The parser is shown in the pg_ts_config entry, but the token-to-dictionary mapping is defined by subsidiary entries in [pg_ts_config_map](#catalog-pg-ts-config-map).

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
   oid `oid`

   Row identifier
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cfgname `name`

   Text search configuration name
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cfgnamespace `oid` (references [pg_namespace](#catalog-pg-namespace).oid)

   The OID of the namespace that contains this configuration
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cfgowner `oid` (references [pg_authid](#catalog-pg-authid).oid)

   Owner of the configuration
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   cfgparser `oid` (references [pg_ts_parser](#catalog-pg-ts-parser).oid)

   The OID of the text search parser for this configuration
  :::{/cell}
  :::{/row}
:::{/table}

: pg_ts_config Columns
