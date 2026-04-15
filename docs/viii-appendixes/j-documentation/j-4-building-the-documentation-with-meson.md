---
title: "J.4. Building the Documentation with Meson"
id: docguide-build-meson
---

## Building the Documentation with Meson

To build the documentation using Meson, change to the `build` directory before running one of these commands, or add `-C build` to the command.

To build just the HTML version of the documentation:

    build$ ninja html

For a list of other documentation targets see [Installation](#installation).
The output appears in the subdirectory `build/doc/src/sgml`.
