m31hst
======

Convenience functions to access and work with HST M31 datasets.

To install:

    pip install -e git+git://github.com/jonathansick/m31hst.git#egg=m31hst


Environment Variables
--------------------

- `$PHATDATA` points to directory with PHAT data sets
- `$BROWNDATA` points to directories for the Brown HLSP datasets.

The PHAT data set can be downloaded from [http://archive.stsci.edu/missions/hlsp/phat/]() and the Brown et al HLSP can be downloaded from [https://archive.stsci.edu/prepds/andromeda/datalist.html]().

- `$PHATV2DATA` points to a directory with the v2 photometry. This can be downloaded using `wget` with the URL list in the `download_lists/` directory of this repo.
    
Info
----

Copyright 2013-2015, Jonathan Sick. BSD Licensed.
