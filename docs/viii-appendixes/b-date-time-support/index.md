---
title: B. Date/Time Support
id: datetime-appendix
---

PostgreSQL uses an internal heuristic parser for all date/time input support.
Dates and times are input as strings, and are broken up into distinct fields with a preliminary determination of what kind of information can be in the field.
Each field is interpreted and either assigned a numeric value, ignored, or rejected.
The parser contains internal lookup tables for all textual fields, including months, days of the week, and time zones.

This appendix includes information on the content of these lookup tables and describes the steps used by the parser to decode dates and times.
