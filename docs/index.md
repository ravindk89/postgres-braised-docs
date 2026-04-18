---
title: (Unofficial) PostgreSQL 18 Documentation
id: home
---

This is a showcase project that uses a well-known documentation corpus (PostGreSQL) to create an unofficial Markdown-based documentation site.

This project in particular uses [Braised Docs](https://ravindkumar.com/braised-docs?ref=internal), a personal project that aims to bring pieces of various docs tooling I've used over the years and merge them with features that I've long since wanted.
In context of this project, it automatically vectorized the docs into ChromaDB and serves access via an MCP server.
The entire circle - building, hosting, vectorizing, and MCP connection - all come entirely from the docs pipeline.

The Braised paradigm is that documentation is a first-class part of the AI-augmented product experience.
Technical writers act as orchestrators who wield AI tooling as a force multiplier, doing more work at scale while maintaining high standards of content.

The human remains key here in ensuring the content that both human and AI readers consume has a baseline of quality associated to it.
The alternative is AI outsourcing which by its nature moves towards the average, which feeds average insight, average outputs, and average experiences.
And in a world of generatively average-as-a-service apps, your product becomes less appealing to anyone who is looking for something more.

I firmly believe that great documentation curated by talented writers is the key in differentiating great products from the scads of AI-generated services heaved out across the internet on a daily basis.
If this tool helps you take a step towards that, drop me a line and I'd be happy to hear what you accomplished.

BraiseDocs is still in development, but anyone who is interested can read up on its [documentation](#TODO) and download the binary to experiment with.
If you do use it, I hope that it helps you in one way or another to adapt to the current wave of change moving through the software industry.

::: {.callout type=important}

A significant amount of the migration was done using a combination of Pandoc, python scripts, and sheer AI-fueled audacity.
There's a lot that's broken post-migration, and while I'm fixing what I can as I go, this project is not intended to be a perfect reproduction.
It's a Proof-of-Concept, and if your preferred agent can pull from these docs using RAG/MCP-isms (and ideally it helps you get your development work done), then it's succeeded in that goal. 

:::

## Neat technical details

BraiseDocs doesn't do embedding itself - it uses a simple pipeline structure to push data to an embedding model, and then guide that stream into a vectorDB.

For this particular site, I used `nomic-embed-text` and `chromadb` computed on a AMD 9070XT using ollama and vulkan extensions.
The ChromaDB data is enhanced with a BM25 search model to help improve the quality of chunk rankings returned.
The full pipeline/hosting isn't in place yet, but it works in practice, and I'll update this section when it's all done and working.

Braised chunks data such that it works to preserve breadcrumbs and heading details, so each individual chunk is as closely correlated to the page topic as possible.
It supports chunk 'hinting' to handle sections that the chunking script/tool struggles with, though that feature is unused in this project.

## Disclaimer

You can find the source code for this project at https://github.com/ravindk89/postgres-braised-docs under a matching license (MIT) as the original PostGreSQL docs

All trademarks, logos, copyrights, or other references are the property of PostgreSQL and used here verbatim from the original conversion.
No usage of any of the above should be considered an endorsement, sponsorship, or approval of this project by the PostgreSQL Community Association of Canada, PostgreSQL Global Development Group, PostgreSQL Project, PostgreSQL Core Team, or PostgreSQL Community.


## Browse the docs

- [Preface](braised:ref/preface) — What PostgreSQL is, its history, and how to report bugs
- [I. Tutorial](braised:ref/tutorial) — Getting started with PostgreSQL
- [II. The SQL Language](braised:ref/sql) — SQL syntax, queries, and data types
- [III. Server Administration](braised:ref/admin) — Installation, configuration, and operations
- [IV. Client Interfaces](braised:ref/client-interfaces) — libpq, ECPG, and other client APIs
- [V. Server Programming](braised:ref/server-programming) — Extending PostgreSQL with functions, triggers, and more
- [VI. Reference](braised:ref/reference) — SQL commands and utility program references
- [VII. Internals](braised:ref/internals) — How PostgreSQL works under the hood
- [VIII. Appendixes](braised:ref/appendixes) — Error codes, date/time support, and other references

