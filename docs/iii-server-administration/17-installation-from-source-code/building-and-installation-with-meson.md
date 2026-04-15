---
title: "17.4. Building and Installation with Meson"
id: install-meson
---

## Building and Installation with Meson

### Short Version

```
meson setup build --prefix=/usr/local/pgsql
cd build
ninja
su
ninja install
adduser postgres
mkdir -p /usr/local/pgsql/data
chown postgres /usr/local/pgsql/data
su - postgres
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test
/usr/local/pgsql/bin/psql test
```

The long version is the rest of this section.

### Installation Procedure

1.  **Configuration** — The first step of the installation procedure is to configure the build tree for your system and choose the options you would like. To create and configure the build directory, you can start with the `meson setup` command.

        meson setup build

    The setup command takes a `builddir` and a `srcdir` argument. If no `srcdir` is given, Meson will deduce the `srcdir` based on the current directory and the location of `meson.build`. The `builddir` is mandatory.

    Running `meson setup` loads the build configuration file and sets up the build directory. Additionally, you can also pass several build options to Meson. Some commonly used options are mentioned in the subsequent sections. For example:

        # configure with a different installation prefix
        meson setup build --prefix=/home/user/pg-install

        # configure to generate a debug build
        meson setup build --buildtype=debug

        # configure to build with OpenSSL support
        meson setup build -Dssl=openssl

    Setting up the build directory is a one-time step. To reconfigure before a new build, you can simply use the `meson configure` command

        meson configure -Dcassert=true

    `meson configure`\'s commonly used command-line options are explained in [Options](#meson-options).

2.  **Build** — By default, Meson uses the [Ninja](https://ninja-build.org/) build tool. To build PostgreSQL from source using Meson, you can simply use the `ninja` command in the build directory.

        ninja

    Ninja will automatically detect the number of CPUs in your computer and parallelize itself accordingly. You can override the number of parallel processes used with the command line argument `-j`.

    It should be noted that after the initial configure step, `ninja` is the only command you ever need to type to compile. No matter how you alter your source tree (short of moving it to a completely new location), Meson will detect the changes and regenerate itself accordingly. This is especially handy if you have multiple build directories. Often one of them is used for development (the \"debug\" build) and others only every now and then (such as a \"static analysis\" build). Any configuration can be built just by cd\'ing to the corresponding directory and running Ninja.

    If you\'d like to build with a backend other than ninja, you can use configure with the `--backend` option to select the one you want to use and then build using `meson compile`. To learn more about these backends and other arguments you can provide to ninja, you can refer to the [Meson documentation](https://mesonbuild.com/Running-Meson.html#building-from-the-source).

3.  **Regression Tests** — If you want to test the newly built server before you install it, you can run the regression tests at this point. The regression tests are a test suite to verify that PostgreSQL runs on your machine in the way the developers expected it to. Type:

        meson test

    (This won\'t work as root; do it as an unprivileged user.) See [Regression Tests](#regression-tests) for detailed information about interpreting the test results. You can repeat this test at any later time by issuing the same command.

    To run pg_regress and pg_isolation_regress tests against a running postgres instance, specify `--setup running` as an argument to `meson test`.

4.  **Installing the Files**

    :::{.callout type="note"}
    If you are upgrading an existing system be sure to read [Upgrading a PostgreSQL Cluster](braised:ref/upgrading), which has instructions about upgrading a cluster.
    :::

    Once PostgreSQL is built, you can install it by simply running the `ninja install` command.

        ninja install

    This will install files into the directories that were specified in Configuration. Make sure that you have appropriate permissions to write into that area. You might need to do this step as root. Alternatively, you can create the target directories in advance and arrange for appropriate permissions to be granted. The standard installation provides all the header files needed for client application development as well as for server-side program development, such as custom functions or data types written in C.

    `ninja install` should work for most cases, but if you\'d like to use more options (such as `--quiet` to suppress extra output), you could also use `meson install` instead. You can learn more about [meson install](https://mesonbuild.com/Commands.html#install) and its options in the Meson documentation.

**Uninstallation:**

To undo the installation, you can use the `ninja uninstall` command.

**Cleaning:**

After the installation, you can free disk space by removing the built files from the source tree with the `ninja clean` command.

### `meson setup` Options

`meson setup`\'s command-line options are explained below.
This list is not exhaustive (use `meson configure --help` to get one that is).
The options not covered here are meant for advanced use-cases, and are documented in the standard [Meson documentation](https://mesonbuild.com/Commands.html#configure).
These arguments can be used with `meson setup` as well.

#### Installation Locations

These options control where `ninja install` (or `meson install`) will put the files.
The `--prefix` option (example [Short Version](#install-short-meson)) is sufficient for most cases.
If you have special needs, you can customize the installation subdirectories with the other options described in this section.
Beware however that changing the relative locations of the different subdirectories may render the installation non-relocatable, meaning you won\'t be able to move it after installation. (The `man` and `doc` locations are not affected by this restriction.) For relocatable installs, you might want to use the `-Drpath=false` option described later.

:::{.dl}
:::{.item term="`--prefix=PREFIX`"}
Install all files under the directory *PREFIX* instead of `/usr/local/pgsql` (on Unix based systems) or `current drive letter:/usr/local/pgsql` (on Windows). The actual files will be installed into various subdirectories; no files will ever be installed directly into the *PREFIX* directory.
:::{/item}
:::{.item term="`--bindir=DIRECTORY`"}
Specifies the directory for executable programs. The default is `PREFIX/bin`.
:::{/item}
:::{.item term="`--sysconfdir=DIRECTORY`"}
Sets the directory for various configuration files, `PREFIX/etc` by default.
:::{/item}
:::{.item term="`--libdir=DIRECTORY`"}
Sets the location to install libraries and dynamically loadable modules. The default is `PREFIX/lib`.
:::{/item}
:::{.item term="`--includedir=DIRECTORY`"}
Sets the directory for installing C and C++ header files. The default is `PREFIX/include`.
:::{/item}
:::{.item term="`--datadir=DIRECTORY`"}
Sets the directory for read-only data files used by the installed programs. The default is `PREFIX/share`. Note that this has nothing to do with where your database files will be placed.
:::{/item}
:::{.item term="`--localedir=DIRECTORY`"}
Sets the directory for installing locale data, in particular message translation catalog files. The default is `DATADIR/locale`.
:::{/item}
:::{.item term="`--mandir=DIRECTORY`"}
The man pages that come with PostgreSQL will be installed under this directory, in their respective `manx` subdirectories. The default is `DATADIR/man`.
:::{/item}
:::{/dl}

:::{.callout type="note"}
Care has been taken to make it possible to install PostgreSQL into shared installation locations (such as `/usr/local/include`) without interfering with the namespace of the rest of the system. First, the string "`/postgresql`" is automatically appended to `datadir`, `sysconfdir`, and `docdir`, unless the fully expanded directory name already contains the string "`postgres`" or "`pgsql`". For example, if you choose `/usr/local` as prefix, the documentation will be installed in `/usr/local/doc/postgresql`, but if the prefix is `/opt/postgres`, then it will be in `/opt/postgres/doc`. The public C header files of the client interfaces are installed into `includedir` and are namespace-clean. The internal header files and the server header files are installed into private directories under `includedir`. See the documentation of each interface for information about how to access its header files. Finally, a private subdirectory will also be created, if appropriate, under `libdir` for dynamically loadable modules.
:::

#### PostgreSQL Features

The options described in this section enable building of various optional PostgreSQL features.
Most of these require additional software, as described in [Requirements](braised:ref/install-requirements), and will be automatically enabled if the required software is found.
You can change this behavior by manually setting these features to `enabled` to require them or `disabled` to not build with them.

To specify PostgreSQL-specific options, the name of the option must be prefixed by `-D`.

:::{.dl}
:::{.item term="`-Dnls={ auto | enabled | disabled }`"}
Enables or disables Native Language Support (NLS), that is, the ability to display a program\'s messages in a language other than English. Defaults to auto and will be enabled automatically if an implementation of the Gettext API is found.
:::{/item}
:::{.item term="`-Dplperl={ auto | enabled | disabled }`"}
Build the PL/Perl server-side language. Defaults to auto.
:::{/item}
:::{.item term="`-Dplpython={ auto | enabled | disabled }`"}
Build the PL/Python server-side language. Defaults to auto.
:::{/item}
:::{.item term="`-Dpltcl={ auto | enabled | disabled }`"}
Build the PL/Tcl server-side language. Defaults to auto.
:::{/item}
:::{.item term="`-Dtcl_version=TCL_VERSION`"}
Specifies the Tcl version to use when building PL/Tcl.
:::{/item}
:::{.item term="`-Dicu={ auto | enabled | disabled }`"}
Build with support for the ICU[Collation Support](braised:ref/collation)). Defaults to auto and requires the ICU4C package to be installed. The minimum required version of ICU4C is currently 4.2.
:::{/item}
:::{.item term="`-Dllvm={ auto | enabled | disabled }`"}
Build with support for LLVM based JIT compilation (see [Just-in-Time Compilation (JIT)](#just-in-time-compilation-jit)). This requires the LLVM library to be installed. The minimum required version of LLVM is currently 14. Disabled by default.

`llvm-config``llvm-config`, and then `llvm-config-$version` for all supported versions, will be searched for in your `PATH`. If that would not yield the desired program, use `LLVM_CONFIG` to specify a path to the correct `llvm-config`.
:::{/item}
:::{.item term="`-Dlz4={ auto | enabled | disabled }`"}
Build with LZ4 compression support. Defaults to auto.
:::{/item}
:::{.item term="`-Dzstd={ auto | enabled | disabled }`"}
Build with Zstandard compression support. Defaults to auto.
:::{/item}
:::{.item term="`-Dssl={ auto | LIBRARY }`"}
Build with support for SSL (encrypted) connections. The only *LIBRARY* supported is `openssl`. This requires the OpenSSL package to be installed. Building with this will check for the required header files and libraries to make sure that your OpenSSL installation is sufficient before proceeding. The default for this option is auto.
:::{/item}
:::{.item term="`-Dgssapi={ auto | enabled | disabled }`"}
Build with support for GSSAPI authentication. MIT Kerberos is required to be installed for GSSAPI. On many systems, the GSSAPI system (a part of the MIT Kerberos installation) is not installed in a location that is searched by default (e.g., `/usr/include`, `/usr/lib`). In those cases, PostgreSQL will query `pkg-config` to detect the required compiler and linker options. Defaults to auto. `meson configure` will check for the required header files and libraries to make sure that your GSSAPI installation is sufficient before proceeding.
:::{/item}
:::{.item term="`-Dldap={ auto | enabled | disabled }`"}
Build with LDAP[[LDAP Lookup of Connection Parameters](braised:ref/libpq-ldap) and [LDAP Authentication](braised:ref/auth-ldap)] for more information). On Unix, this requires the OpenLDAP package to be installed. On Windows, the default WinLDAP library is used. Defaults to auto. `meson configure` will check for the required header files and libraries to make sure that your OpenLDAP installation is sufficient before proceeding.
:::{/item}
:::{.item term="`-Dpam={ auto | enabled | disabled }`"}
Build with PAM
:::{/item}
:::{.item term="`-Dbsd_auth={ auto | enabled | disabled }`"}
Build with BSD Authentication support. (The BSD Authentication framework is currently only available on OpenBSD.) Defaults to auto.
:::{/item}
:::{.item term="`-Dsystemd={ auto | enabled | disabled }`"}
Build with support for systemdsystemd but has no impact otherwise; see [Starting the Database Server](braised:ref/server-start) for more information. Defaults to auto. libsystemd and the associated header files need to be installed to use this option.
:::{/item}
:::{.item term="`-Dbonjour={ auto | enabled | disabled }`"}
Build with support for Bonjour automatic service discovery. Defaults to auto and requires Bonjour support in your operating system. Recommended on macOS.
:::{/item}
:::{.item term="`-Duuid=LIBRARY`"}
Build the [F.49. uuid-ossp — a UUID generator](braised:ref/uuid-ossp) module (which provides functions to generate UUIDs), using the specified UUID library.*LIBRARY* must be one of:

-   `none` to not build the uuid module. This is the default.

-   `bsd` to use the UUID functions found in FreeBSD, and some other BSD-derived systems

-   `e2fs` to use the UUID library created by the `e2fsprogs` project; this library is present in most Linux systems and in macOS, and can be obtained for other platforms as well

-   `ossp` to use the [OSSP UUID library](http://www.ossp.org/pkg/lib/uuid/)
:::{/item}
:::{.item term="`-Dlibcurl={ auto | enabled | disabled }`"}
Build with libcurl support for OAuth 2.0 client flows. Libcurl version 7.61.0 or later is required for this feature. Building with this will check for the required header files and libraries to make sure that your Curl installation is sufficient before proceeding. The default for this option is auto.
:::{/item}
:::{.item term="`-Dliburing={ auto | enabled | disabled }`"}
Build with liburing, enabling io_uring support for asynchronous I/O. Defaults to auto.

To use a liburing installation that is in an unusual location, you can set `pkg-config`-related environment variables (see its documentation).
:::{/item}
:::{.item term="`-Dlibnuma={ auto | enabled | disabled }`"}
Build with libnuma support for basic NUMA support. Only supported on platforms for which the libnuma library is implemented. The default for this option is auto.
:::{/item}
:::{.item term="`-Dlibxml={ auto | enabled | disabled }`"}
Build with libxml2, enabling SQL/XML support. Defaults to auto. Libxml2 version 2.6.23 or later is required for this feature.

To use a libxml2 installation that is in an unusual location, you can set `pkg-config`-related environment variables (see its documentation).
:::{/item}
:::{.item term="`-Dlibxslt={ auto | enabled | disabled }`"}
Build with libxslt, enabling the [F.50. xml2 — XPath querying and XSLT functionality](braised:ref/xml2) module to perform XSL transformations of XML. `-Dlibxml` must be specified as well. Defaults to auto.
:::{/item}
:::{.item term="`-Dselinux={ auto | enabled | disabled }`"}
Build with SElinux support, enabling the [F.40. sepgsql — SELinux-, label-based mandatory access control (MAC) security module](braised:ref/sepgsql) extension. Defaults to auto.
:::{/item}
:::{/dl}

#### Anti-Features

:::{.dl}
:::{.item term="`-Dreadline={ auto | enabled | disabled }`"}
Allows use of the Readline library (and libedit as well). This option defaults to auto and enables command-line editing and history in psql and is strongly recommended.
:::{/item}
:::{.item term="`-Dlibedit_preferred={ true | false }`"}
Setting this to true favors the use of the BSD-licensed libedit library rather than GPL-licensed Readline. This option is significant only if you have both libraries installed; the default is false, that is to use Readline.
:::{/item}
:::{.item term="`-Dzlib={ auto | enabled | disabled }`"}
Zlib library. It defaults to auto and enables support for compressed archives in pg_dump, pg_restore and pg_basebackup and is recommended.
:::{/item}
:::{/dl}

#### Build Process Details

:::{.dl}
:::{.item term="`--auto-features={ auto | enabled | disabled }`"}
Setting this option allows you to override the value of all "auto" features (features that are enabled automatically if the required software is found). This can be useful when you want to disable or enable all the "optional" features at once without having to set each of them manually. The default value for this parameter is auto.
:::{/item}
:::{.item term="`--backend=BACKEND`"}
The default backend Meson uses is ninja and that should suffice for most use cases. However, if you\'d like to fully integrate with Visual Studio, you can set the *BACKEND* to `vs`.
:::{/item}
:::{.item term="`-Dc_args=OPTIONS`"}
This option can be used to pass extra options to the C compiler.
:::{/item}
:::{.item term="`-Dc_link_args=OPTIONS`"}
This option can be used to pass extra options to the C linker.
:::{/item}
:::{.item term="`-Dextra_include_dirs=DIRECTORIES`"}
*DIRECTORIES* is a comma-separated list of directories that will be added to the list the compiler searches for header files. If you have optional packages (such as GNU Readline) installed in a non-standard location, you have to use this option and probably also the corresponding `-Dextra_lib_dirs` option.

Example: `-Dextra_include_dirs=/opt/gnu/include,/usr/sup/include`.
:::{/item}
:::{.item term="`-Dextra_lib_dirs=DIRECTORIES`"}
*DIRECTORIES* is a comma-separated list of directories to search for libraries. You will probably have to use this option (and the corresponding `-Dextra_include_dirs` option) if you have packages installed in non-standard locations.

Example: `-Dextra_lib_dirs=/opt/gnu/lib,/usr/sup/lib`.
:::{/item}
:::{.item term="`-Dsystem_tzdata=DIRECTORY`"}
PostgreSQL includes its own time zone database, which it requires for date and time operations. This time zone database is in fact compatible with the IANA time zone database provided by many operating systems such as FreeBSD, Linux, and Solaris, so it would be redundant to install it again. When this option is used, the system-supplied time zone database in *DIRECTORY* is used instead of the one included in the PostgreSQL source distribution. *DIRECTORY* must be specified as an absolute path. `/usr/share/zoneinfo` is a likely directory on some operating systems. Note that the installation routine will not detect mismatching or erroneous time zone data. If you use this option, you are advised to run the regression tests to verify that the time zone data you have pointed to works correctly with PostgreSQL.

This option is mainly aimed at binary package distributors who know their target operating system well. The main advantage of using this option is that the PostgreSQL package won\'t need to be upgraded whenever any of the many local daylight-saving time rules change. Another advantage is that PostgreSQL can be cross-compiled more straightforwardly if the time zone database files do not need to be built during the installation.
:::{/item}
:::{.item term="`-Dextra_version=STRING`"}
Append *STRING* to the PostgreSQL version number. You can use this, for example, to mark binaries built from unreleased Git snapshots or containing custom patches with an extra version string, such as a `git describe` identifier or a distribution package release number.
:::{/item}
:::{.item term="`-Drpath={ true | false }`"}
This option is set to true by default. If set to false, do not mark PostgreSQL\'s executables to indicate that they should search for shared libraries in the installation\'s library directory (see `--libdir`). On most platforms, this marking uses an absolute path to the library directory, so that it will be unhelpful if you relocate the installation later. However, you will then need to provide some other way for the executables to find the shared libraries. Typically this requires configuring the operating system\'s dynamic linker to search the library directory; see [Shared Libraries](braised:ref/install-post#shared-libraries) for more detail.
:::{/item}
:::{.item term="`-DBINARY_NAME=PATH`"}
If a program required to build PostgreSQL (with or without optional flags) is stored at a non-standard path, you can specify it manually to `meson configure`. The complete list of programs for which this is supported can be found by running `meson configure`. Example:

    meson configure -DBISON=PATH_TO_BISON
:::{/item}
:::{/dl}

#### Documentation

See [J.2. Tool Sets](braised:ref/docguide-toolsets) for the tools needed for building the documentation.

:::{.dl}
:::{.item term="`-Ddocs={ auto | enabled | disabled }`"}
Enables building the documentation in HTML and man format. It defaults to auto.
:::{/item}
:::{.item term="`-Ddocs_pdf={ auto | enabled | disabled }`"}
Enables building the documentation in PDF format. It defaults to auto.
:::{/item}
:::{.item term="`-Ddocs_html_style={ simple | website }`"}
Controls which CSS stylesheet is used. The default is `simple`. If set to `website`, the HTML documentation will reference the stylesheet for [postgresql.org](https://www.postgresql.org/docs/current/).
:::{/item}
:::{/dl}

#### Miscellaneous

:::{.dl}
:::{.item term="`-Dpgport=NUMBER`"}
Set *NUMBER* as the default port number for server and clients. The default is 5432. The port can always be changed later on, but if you specify it here then both server and clients will have the same default compiled in, which can be very convenient. Usually the only good reason to select a non-default value is if you intend to run multiple PostgreSQL servers on the same machine.
:::{/item}
:::{.item term="`-Dkrb_srvnam=NAME`"}
The default name of the Kerberos service principal used by GSSAPI. `postgres` is the default. There\'s usually no reason to change this unless you are building for a Windows environment, in which case it must be set to upper case `POSTGRES`.
:::{/item}
:::{.item term="`-Dsegsize=SEGSIZE`"}
Set the segment size, in gigabytes. Large tables are divided into multiple operating-system files, each of size equal to the segment size. This avoids problems with file size limits that exist on many platforms. The default segment size, 1 gigabyte, is safe on all supported platforms. If your operating system has "largefile" support (which most do, nowadays), you can use a larger segment size. This can be helpful to reduce the number of file descriptors consumed when working with very large tables. But be careful not to select a value larger than is supported by your platform and the file systems you intend to use. Other tools you might wish to use, such as tar, could also set limits on the usable file size. It is recommended, though not absolutely required, that this value be a power of 2.
:::{/item}
:::{.item term="`-Dblocksize=BLOCKSIZE`"}
Set the block size, in kilobytes. This is the unit of storage and I/O within tables. The default, 8 kilobytes, is suitable for most situations; but other values may be useful in special cases. The value must be a power of 2 between 1 and 32 (kilobytes).
:::{/item}
:::{.item term="`-Dwal_blocksize=BLOCKSIZE`"}
Set the WAL block size, in kilobytes. This is the unit of storage and I/O within the WAL log. The default, 8 kilobytes, is suitable for most situations; but other values may be useful in special cases. The value must be a power of 2 between 1 and 64 (kilobytes).
:::{/item}
:::{/dl}

#### Developer Options

Most of the options in this section are only of interest for developing or debugging PostgreSQL.
They are not recommended for production builds, except for `--debug`, which can be useful to enable detailed bug reports in the unlucky event that you encounter a bug.
On platforms supporting DTrace, `-Ddtrace` may also be reasonable to use in production.

When building an installation that will be used to develop code inside the server, it is recommended to use at least the `--buildtype=debug` and `-Dcassert` options.

:::{.dl}
:::{.item term="`--buildtype=BUILDTYPE`"}
This option can be used to specify the buildtype to use; defaults to `debugoptimized`. If you\'d like finer control on the debug symbols and optimization levels than what this option provides, you can refer to the `--debug` and `--optimization` flags.

The following build types are generally used: `plain`, `debug`, `debugoptimized` and `release`. More information about them can be found in the [Meson documentation](https://mesonbuild.com/Running-Meson.html#configuring-the-build-directory).
:::{/item}
:::{.item term="`--debug`"}
Compiles all programs and libraries with debugging symbols. This means that you can run the programs in a debugger to analyze problems. This enlarges the size of the installed executables considerably, and on non-GCC compilers it usually also disables compiler optimization, causing slowdowns. However, having the symbols available is extremely helpful for dealing with any problems that might arise. Currently, this option is recommended for production installations only if you use GCC. But you should always have it on if you are doing development work or running a beta version.
:::{/item}
:::{.item term="`--optimization`=*LEVEL*"}
Specify the optimization level. `LEVEL` can be set to any of {0,g,1,2,3,s}.
:::{/item}
:::{.item term="`--werror`"}
Setting this option asks the compiler to treat warnings as errors. This can be useful for code development.
:::{/item}
:::{.item term="`-Dcassert={ true | false }`"}
Enables assertion checks in the server, which test for many "cannot happen" conditions. This is invaluable for code development purposes, but the tests slow down the server significantly. Also, having the tests turned on won\'t necessarily enhance the stability of your server! The assertion checks are not categorized for severity, and so what might be a relatively harmless bug will still lead to server restarts if it triggers an assertion failure. This option is not recommended for production use, but you should have it on for development work or when running a beta version.
:::{/item}
:::{.item term="`-Dtap_tests={ auto | enabled | disabled }`"}
Enable tests using the Perl TAP tools. Defaults to auto and requires a Perl installation and the Perl module `IPC::Run`. See [TAP Tests](braised:ref/regress-tap) for more information.
:::{/item}
:::{.item term="`-DPG_TEST_EXTRA=TEST_SUITES`"}
Enable additional test suites, which are not run by default because they are not secure to run on a multiuser system, require special software to run, or are resource intensive. The argument is a whitespace-separated list of tests to enable. See [Additional Test Suites](braised:ref/regress-run#additional-test-suites) for details. If the `PG_TEST_EXTRA` environment variable is set when the tests are run, it overrides this setup-time option.
:::{/item}
:::{.item term="`-Db_coverage={ true | false }`"}
If using GCC, all programs and libraries are compiled with code coverage testing instrumentation. When run, they generate files in the build directory with code coverage metrics. See [Test Coverage Examination](braised:ref/regress-coverage) for more information. This option is for use only with GCC and when doing development work.
:::{/item}
:::{.item term="`-Ddtrace={ auto | enabled | disabled }`"}
PostgreSQL with support for the dynamic tracing tool DTrace. See [Dynamic Tracing](braised:ref/dynamic-trace) for more information.

To point to the `dtrace` program, the `DTRACE` option can be set. This will often be necessary because `dtrace` is typically installed under `/usr/sbin`, which might not be in your `PATH`.
:::{/item}
:::{.item term="`-Dinjection_points={ true | false }`"}
Compiles PostgreSQL with support for injection points in the server. Injection points allow to run user-defined code from within the server in pre-defined code paths. This helps in testing and in the investigation of concurrency scenarios in a controlled fashion. This option is disabled by default. See [Injection Points](braised:ref/xfunc-c#injection-points) for more details. This option is intended to be used only by developers for testing.
:::{/item}
:::{.item term="`-Dsegsize_blocks=SEGSIZE_BLOCKS`"}
Specify the relation segment size in blocks. If both `-Dsegsize` and this option are specified, this option wins. This option is only for developers, to test segment related code.
:::{/item}
:::{/dl}

### `meson` Build Targets

Individual build targets can be built using `ninja` *target*.
When no target is specified, everything except documentation is built.
Individual build products can be built using the path/filename as *target*.
