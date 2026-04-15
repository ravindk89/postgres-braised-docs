---
title: "50.2. Initialization Functions"
id: oauth-validator-init
---

## Initialization Functions

OAuth validator modules are dynamically loaded from the shared libraries listed in [oauth_validator_libraries (string)
      
       oauth_validator_libraries configuration parameter](braised:ref/runtime-config-connection#oauth-validator-libraries-string-oauth-validator-libraries-configuration-parameter). Modules are loaded on demand when requested from a login in progress. The normal library search path is used to locate the library. To provide the validator callbacks and to indicate that the library is an OAuth validator module a function named `_PG_oauth_validator_module_init` must be provided. The return value of the function must be a pointer to a struct of type OAuthValidatorCallbacks, which contains a magic number and pointers to the module\'s token validation functions. The returned pointer must be of server lifetime, which is typically achieved by defining it as a `static const` variable in global scope.

    typedef struct OAuthValidatorCallbacks
    {
        uint32        magic;            /* must be set to PG_OAUTH_VALIDATOR_MAGIC */

        ValidatorStartupCB startup_cb;
        ValidatorShutdownCB shutdown_cb;
        ValidatorValidateCB validate_cb;
    } OAuthValidatorCallbacks;

    typedef const OAuthValidatorCallbacks *(*OAuthValidatorModuleInit) (void);

Only the `validate_cb` callback is required, the others are optional.
