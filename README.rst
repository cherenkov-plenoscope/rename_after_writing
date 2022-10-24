Network-File-System
===================
|BlackStyle|

A python-library to make moves, copys and writes safer on remote drives.
Writing a file is not atomic. In the worst case the process writing your file
dies while the file is not complete. To at least spot such incomplete files,
all writing-operations (write, move, copy, ...) will be followed by an
atomic move.

.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
