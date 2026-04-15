---
title: "52.1. Overview"
id: catalogs-overview
---

## Overview

System Catalogs lists the system catalogs.
More detailed documentation of each catalog follows below.

Most system catalogs are copied from the template database during database creation and are thereafter database-specific.
A few catalogs are physically shared across all databases in a cluster; these are noted in the descriptions of the individual catalogs.

:::{.table}
  :::{.row header="true"}
  :::{.cell}
  Catalog Name
  :::{/cell}
  :::{.cell}
  Purpose
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_aggregate](#catalog-pg-aggregate)
  :::{/cell}
  :::{.cell}
  aggregate functions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_am](#catalog-pg-am)
  :::{/cell}
  :::{.cell}
  relation access methods
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_amop](#catalog-pg-amop)
  :::{/cell}
  :::{.cell}
  access method operators
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_amproc](#catalog-pg-amproc)
  :::{/cell}
  :::{.cell}
  access method support functions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_attrdef](#catalog-pg-attrdef)
  :::{/cell}
  :::{.cell}
  column default values
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_attribute](#catalog-pg-attribute)
  :::{/cell}
  :::{.cell}
  table columns ("attributes")
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_authid](#catalog-pg-authid)
  :::{/cell}
  :::{.cell}
  authorization identifiers (roles)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_auth_members](#catalog-pg-auth-members)
  :::{/cell}
  :::{.cell}
  authorization identifier membership relationships
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_cast](#catalog-pg-cast)
  :::{/cell}
  :::{.cell}
  casts (data type conversions)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_class](#catalog-pg-class)
  :::{/cell}
  :::{.cell}
  tables, indexes, sequences, views ("relations")
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_collation](#catalog-pg-collation)
  :::{/cell}
  :::{.cell}
  collations (locale information)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_constraint](#catalog-pg-constraint)
  :::{/cell}
  :::{.cell}
  check constraints, unique constraints, primary key constraints, foreign key constraints
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_conversion](#catalog-pg-conversion)
  :::{/cell}
  :::{.cell}
  encoding conversion information
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_database](#catalog-pg-database)
  :::{/cell}
  :::{.cell}
  databases within this database cluster
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_db_role_setting](#catalog-pg-db-role-setting)
  :::{/cell}
  :::{.cell}
  per-role and per-database settings
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_default_acl](#catalog-pg-default-acl)
  :::{/cell}
  :::{.cell}
  default privileges for object types
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_depend](#catalog-pg-depend)
  :::{/cell}
  :::{.cell}
  dependencies between database objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_description](#catalog-pg-description)
  :::{/cell}
  :::{.cell}
  descriptions or comments on database objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_enum](#catalog-pg-enum)
  :::{/cell}
  :::{.cell}
  enum label and value definitions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_event_trigger](#catalog-pg-event-trigger)
  :::{/cell}
  :::{.cell}
  event triggers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_extension](#catalog-pg-extension)
  :::{/cell}
  :::{.cell}
  installed extensions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_foreign_data_wrapper](#catalog-pg-foreign-data-wrapper)
  :::{/cell}
  :::{.cell}
  foreign-data wrapper definitions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_foreign_server](#catalog-pg-foreign-server)
  :::{/cell}
  :::{.cell}
  foreign server definitions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_foreign_table
  :::{/cell}
  :::{.cell}
  additional foreign table information
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_index](#catalog-pg-index)
  :::{/cell}
  :::{.cell}
  additional index information
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_inherits](#catalog-pg-inherits)
  :::{/cell}
  :::{.cell}
  table inheritance hierarchy
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_init_privs](#catalog-pg-init-privs)
  :::{/cell}
  :::{.cell}
  object initial privileges
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_language](#catalog-pg-language)
  :::{/cell}
  :::{.cell}
  languages for writing functions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_largeobject](#catalog-pg-largeobject)
  :::{/cell}
  :::{.cell}
  data pages for large objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_largeobject_metadata](#catalog-pg-largeobject-metadata)
  :::{/cell}
  :::{.cell}
  metadata for large objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_namespace](#catalog-pg-namespace)
  :::{/cell}
  :::{.cell}
  schemas
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_opclass](#catalog-pg-opclass)
  :::{/cell}
  :::{.cell}
  access method operator classes
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_operator](#catalog-pg-operator)
  :::{/cell}
  :::{.cell}
  operators
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_opfamily](#catalog-pg-opfamily)
  :::{/cell}
  :::{.cell}
  access method operator families
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_parameter_acl](#catalog-pg-parameter-acl)
  :::{/cell}
  :::{.cell}
  configuration parameters for which privileges have been granted
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  pg_partitioned_table
  :::{/cell}
  :::{.cell}
  information about partition key of tables
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_policy](#catalog-pg-policy)
  :::{/cell}
  :::{.cell}
  row-security policies
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_proc](#catalog-pg-proc)
  :::{/cell}
  :::{.cell}
  functions and procedures
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_publication](#catalog-pg-publication)
  :::{/cell}
  :::{.cell}
  publications for logical replication
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_publication_namespace](#catalog-pg-publication-namespace)
  :::{/cell}
  :::{.cell}
  schema to publication mapping
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_publication_rel](#catalog-pg-publication-rel)
  :::{/cell}
  :::{.cell}
  relation to publication mapping
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_range](#catalog-pg-range)
  :::{/cell}
  :::{.cell}
  information about range types
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_replication_origin](#catalog-pg-replication-origin)
  :::{/cell}
  :::{.cell}
  registered replication origins
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_rewrite](#catalog-pg-rewrite)
  :::{/cell}
  :::{.cell}
  query rewrite rules
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_seclabel](#catalog-pg-seclabel)
  :::{/cell}
  :::{.cell}
  security labels on database objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_sequence](#catalog-pg-sequence)
  :::{/cell}
  :::{.cell}
  information about sequences
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shdepend](#catalog-pg-shdepend)
  :::{/cell}
  :::{.cell}
  dependencies on shared objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shdescription](#catalog-pg-shdescription)
  :::{/cell}
  :::{.cell}
  comments on shared objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_shseclabel](#catalog-pg-shseclabel)
  :::{/cell}
  :::{.cell}
  security labels on shared database objects
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_statistic](#catalog-pg-statistic)
  :::{/cell}
  :::{.cell}
  planner statistics
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_statistic_ext](#catalog-pg-statistic-ext)
  :::{/cell}
  :::{.cell}
  extended planner statistics (definition)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_statistic_ext_data](#catalog-pg-statistic-ext-data)
  :::{/cell}
  :::{.cell}
  extended planner statistics (built statistics)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_subscription](#catalog-pg-subscription)
  :::{/cell}
  :::{.cell}
  logical replication subscriptions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_subscription_rel](#catalog-pg-subscription-rel)
  :::{/cell}
  :::{.cell}
  relation state for subscriptions
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_tablespace](#catalog-pg-tablespace)
  :::{/cell}
  :::{.cell}
  tablespaces within this database cluster
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_transform](#catalog-pg-transform)
  :::{/cell}
  :::{.cell}
  transforms (data type to procedural language conversions)
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_trigger](#catalog-pg-trigger)
  :::{/cell}
  :::{.cell}
  triggers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ts_config](#catalog-pg-ts-config)
  :::{/cell}
  :::{.cell}
  text search configurations
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ts_config_map](#catalog-pg-ts-config-map)
  :::{/cell}
  :::{.cell}
  text search configurations\' token mappings
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ts_dict](#catalog-pg-ts-dict)
  :::{/cell}
  :::{.cell}
  text search dictionaries
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ts_parser](#catalog-pg-ts-parser)
  :::{/cell}
  :::{.cell}
  text search parsers
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_ts_template](#catalog-pg-ts-template)
  :::{/cell}
  :::{.cell}
  text search templates
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_type](#catalog-pg-type)
  :::{/cell}
  :::{.cell}
  data types
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
  [pg_user_mapping](#catalog-pg-user-mapping)
  :::{/cell}
  :::{.cell}
  mappings of users to foreign servers
  :::{/cell}
  :::{/row}
:::{/table}

  : System Catalogs
