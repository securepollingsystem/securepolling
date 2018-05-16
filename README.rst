Secure Polling
==============
This is a prototype implementation of the
`Secure Polling System <https://securepollingsystem.org>`_ (SPS)
architecture as command line and web utilities.

Usage
-----
See the `documentation <https://thomaslevine.com/scm/securepolling/uv/doc/_build/html/index.html>`_.

Future components
-----------------

sps_server
    Web versions of the three server components of the system, that is,
    the registrar, screed host, and tally host
sps_poller_cli
    Command-line version of the poller that communicates with the
    aforementioned servers
sps_local
    Local version of the system, where "server" addresses are specified
    as paths to SQLite3 databases
securepolling
    Shared Python library
