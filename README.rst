=======
Pycsync
=======

.. image:: https://travis-ci.org/shadowfax-chc/pycsync.svg
    :target: https://travis-ci.org/shadowfax-chc/pycsync
    :alt: Build Status

.. image:: https://coveralls.io/repos/shadowfax-chc/pycsync/badge.png
    :target: https://coveralls.io/r/shadowfax-chc/pycsync
    :alt: Coverage Status

.. image:: https://landscape.io/github/shadowfax-chc/pycsync/master/landscape.png
    :target: https://landscape.io/github/shadowfax-chc/pycsync/master
    :alt: Code Health

.. image:: https://gemnasium.com/shadowfax-chc/pycsync.svg
    :target: https://gemnasium.com/shadowfax-chc/pycsync
    :alt: Dependency Status

Sync pictures between filesystem and Flickr

Install
-------

This uses the python_flickr_api_ (many thanks to `Alexis Mignon`_).

To install latest::

    pip install https://github.com/shadowfax-chc/pycsync/tarball/master


Usage
-----

First oauth needs to be setup for the application::

    pycsync -a

Then copy the link to a browser. After authorizing pycsync copy the
``oauth_verifier`` and input it to pycsync.

``NOTE:`` pycsync can either be run from the sync directory or the directory
can be specified with the ``-p`` option.

Now to sync simply run::

    pycsync


Limitations
-----------

Currently there are several limitaions (Wokring on resolving them).

1. Only syncs a file once. Currently once a file exists, it will not be synced
   if it changes.
2. Requires flat file structure. The file system layout must contain one level
   of directories with files in them. The directories will be mapped to Photo
   Sets. Any subdirectories will be ignored. Also any top-level files will be
   ignored.


.. _python_flickr_api: https://github.com/alexis-mignon/python-flickr-api
.. _Alexis Mignon: https://github.com/alexis-mignon
