---
title: 51. Overview of PostgreSQL Internals
id: overview
---

:::{.callout type="note" title="Author"}
This chapter originated as part of Simkovics [1998] Stefan Simkovics\' Master\'s Thesis prepared at Vienna University of Technology under the direction of O.Univ.Prof.Dr. Georg Gottlob and Univ.Ass.
Mag.
Katrin Seyr.
:::

This chapter gives an overview of the internal structure of the backend of PostgreSQL.
After having read the following sections you should have an idea of how a query is processed.
This chapter is intended to help the reader understand the general sequence of operations that occur within the backend from the point at which a query is received, to the point at which the results are returned to the client.
