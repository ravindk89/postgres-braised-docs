---
title: 69. How the Planner Uses Statistics
id: planner-stats-details
---

This chapter builds on the material covered in [Section 14.1](braised:ref/using-explain) and [Section 14.2](braised:ref/planner-stats) to show some additional details about how the planner uses the system statistics to estimate the number of rows each part of a query might return.
This is a significant part of the planning process, providing much of the raw material for cost calculation.

The intent of this chapter is not to document the code in detail, but to present an overview of how it works.
This will perhaps ease the learning curve for someone who subsequently wishes to read the code.
