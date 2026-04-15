---
title: "47.7. Logical Decoding Output Writers"
id: logicaldecoding-writer
---

## Logical Decoding Output Writers

It is possible to add more output methods for logical decoding.
For details, see `src/backend/replication/logical/logicalfuncs.c`.
Essentially, three functions need to be provided: one to read WAL, one to prepare writing output, and one to write the output (see [Functions for Producing Output](braised:ref/logicaldecoding-output-plugin#functions-for-producing-output)).
