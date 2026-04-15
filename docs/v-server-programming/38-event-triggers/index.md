---
title: 38. Event Triggers
id: event-triggers
---

To supplement the trigger mechanism discussed in [37. Triggers](braised:ref/triggers), PostgreSQL also provides event triggers.
Unlike regular triggers, which are attached to a single table and capture only DML events, event triggers are global to a particular database and are capable of capturing DDL events.

Like regular triggers, event triggers can be written in any procedural language that includes event trigger support, or in C, but not in plain SQL.
