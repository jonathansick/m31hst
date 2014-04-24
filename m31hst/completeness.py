#!/usr/bin/env python
# encoding: utf-8
"""
Compute completeness for the Brown HST dataset given their scattering kernels.
"""

import numpy as np
import astropy.io.fits as fits


def estimate_completeness(m606w, m814w, ast_path):
    """Compute completeness given path to the AST kernel file and magnitudes
    of stars in F606W and F814W bands.

    Parameters
    ----------
    m606w : ndarray
        Array of F606W magnitudes
    m814w : ndarray
        Array of F814W magnitudes
    ast_path : str
        Path to Brown AST data file, obtained from :func:`brown_phot_path`
        with ``kind='ast'`` set.
    """
    astfits = fits.open(ast_path)
    ast = astfits[0].data
    astfits.close()

    # Completeness Hess diagram
    # Shape 91, 16
    # Axis 0 is F814W magnitude in range [31.5, 22.5] in steps of 0.1 mag
    # Axis 1 is F606W-F814W magnitude in range [-1.1,0.4] in steps of 0.1 mag
    c = ast.sum(axis=(0, 1))

    ly = np.linspace(31.5, 22.5, 91)
    lx = np.linspace(-1.1, 0.4, 16)
    ind_y = np.digitize(m814w, ly)
    ind_x = np.digitize(m606w - m814w, lx)
    ind_y[ind_y == 91] = 90  # reset overflow from digitize
    ind_x[ind_x == 16] = 15  # reset overflow from digitize

    completeness = c[ind_y, ind_x]

    return completeness
