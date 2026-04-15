---
title: "30.3. Configuration"
id: jit-configuration
---

## Configuration

The configuration variable [jit (boolean)
      
       jit configuration parameter](braised:ref/runtime-config-query#jit-boolean-jit-configuration-parameter) determines whether JIT compilation is enabled or disabled. If it is enabled, the configuration variables [jit_above_cost (floating point)
      
       jit_above_cost configuration parameter](braised:ref/runtime-config-query#jit-above-cost-floating-point-jit-above-cost-configuration-parameter), [jit_inline_above_cost (floating point)
      
       jit_inline_above_cost configuration parameter](braised:ref/runtime-config-query#jit-inline-above-cost-floating-point-jit-inline-above-cost-configuration-parameter), and [jit_optimize_above_cost (floating point)
      
       jit_optimize_above_cost configuration parameter](braised:ref/runtime-config-query#jit-optimize-above-cost-floating-point-jit-optimize-above-cost-configuration-parameter) determine whether JIT compilation is performed for a query, and how much effort is spent doing so.

[jit_provider (string)
       
        jit_provider configuration parameter](braised:ref/runtime-config-client#jit-provider-string-jit-provider-configuration-parameter) determines which JIT implementation is used. It is rarely required to be changed. See [Pluggable JIT Providers](braised:ref/jit-extensibility#pluggable-jit-providers).

For development and debugging purposes a few additional configuration parameters exist, as described in [Developer Options](braised:ref/runtime-config-developer).
