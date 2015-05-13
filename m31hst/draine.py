#!/usr/bin/env python
# encoding: utf-8
"""
Access to the Draine M31 dust maps.

2015-05-12 - Created by Jonathan Sick
"""

import os

from m31hst.paths import MissingData


def spire350_dust_mass_map():
    """Path to the Draine et al 2014 dust mass map.

    See http://www.astro.princeton.edu/~draine/m31dust/m31dust.html
    """
    path = os.path.join(os.getenv('DRAINEDATA', None),
                        'M31_S350_110_SSS_110_Model_All_SurfBr_Mdust.fits.gz')
    if not os.path.exists(path):
        raise MissingData('{0} not found'.format(path))
    return path
