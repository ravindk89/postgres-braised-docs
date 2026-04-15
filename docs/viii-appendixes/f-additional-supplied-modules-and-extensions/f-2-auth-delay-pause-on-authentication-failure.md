---
title: "F.2. auth_delay — pause on authentication failure"
id: auth-delay
---

## auth_delay pause on authentication failure

`auth_delay` causes the server to pause briefly before reporting authentication failure, to make brute-force attacks on database passwords more difficult.
Note that it does nothing to prevent denial-of-service attacks, and may even exacerbate them, since processes that are waiting before reporting authentication failure will still consume connection slots.

In order to function, this module must be loaded via [shared_preload_libraries (string)
      
       shared_preload_libraries configuration parameter](braised:ref/runtime-config-client#shared-preload-libraries-string-shared-preload-libraries-configuration-parameter) in `postgresql.conf`.

### Configuration Parameters

:::{.dl}
:::{.item term="`auth_delay.milliseconds` (`integer`)"}
The number of milliseconds to wait before reporting an authentication failure. The default is 0.
:::{/item}
:::{/dl}

These parameters must be set in `postgresql.conf`.
Typical usage might be:

    # postgresql.conf
    shared_preload_libraries = 'auth_delay'

    auth_delay.milliseconds = '500'

### Author

KaiGai Kohei <kaigai@ak.jp.nec.com>
