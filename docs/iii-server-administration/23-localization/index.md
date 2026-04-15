---
title: 23. Localization
id: charset
---

This chapter describes the available localization features from the point of view of the administrator.
PostgreSQL supports two localization facilities:

-   Using the locale features of the operating system to provide locale-specific collation order, number formatting, translated messages, and other aspects. This is covered in [Section 23.1](braised:ref/locale) and [Section 23.2](braised:ref/collation).

-   Providing a number of different character sets to support storing text in all kinds of languages, and providing character set translation between client and server. This is covered in [Section 23.3](braised:ref/multibyte).
