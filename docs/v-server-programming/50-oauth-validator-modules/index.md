---
title: 50. OAuth Validator Modules
id: oauth-validators
---

PostgreSQL provides infrastructure for creating custom modules to perform server-side validation of OAuth bearer tokens.
Because OAuth implementations vary so wildly, and bearer token validation is heavily dependent on the issuing party, the server cannot check the token itself; validator modules provide the integration layer between the server and the OAuth provider in use.

OAuth validator modules must at least consist of an initialization function (see [Section 50.2](braised:ref/oauth-validator-init)) and the required callback for performing validation (see [Section 50.3](braised:ref/oauth-validator-callbacks)).

:::{.callout type="warning"}
Since a misbehaving validator might let unauthorized users into the database, correct implementation is crucial for server safety.
See [Section 50.1](braised:ref/oauth-validator-design) for design considerations.
:::
