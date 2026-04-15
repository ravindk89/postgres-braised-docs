---
title: "35.2. Data Types"
id: infoschema-datatypes
---

## Data Types

The columns of the information schema views use special data types that are defined in the information schema.
These are defined as simple domains over ordinary built-in types.
You should not use these types for work outside the information schema, but your applications must be prepared for them if they select from the information schema.

These types are:

:::{.dl}
:::{.item term="`cardinal_number`"}
A nonnegative integer.
:::{/item}
:::{.item term="`character_data`"}
A character string (without specific maximum length).
:::{/item}
:::{.item term="`sql_identifier`"}
A character string. This type is used for SQL identifiers, the type `character_data` is used for any other kind of text data.
:::{/item}
:::{.item term="`time_stamp`"}
A domain over the type `timestamp with time zone`
:::{/item}
:::{.item term="`yes_or_no`"}
A character string domain that contains either `YES` or `NO`. This is used to represent Boolean (true/false) data in the information schema. (The information schema was invented before the type `boolean` was added to the SQL standard, so this convention is necessary to keep the information schema backward compatible.)
:::{/item}
:::{/dl}

Every column in the information schema has one of these five types.
