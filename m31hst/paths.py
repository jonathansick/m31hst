#!/usr/bin/env python
# encoding: utf-8
"""
Access to HST data sets.

The environment variables $PHATDATA and $BROWNDATA should point to root
directories for the PHAT and Brown HLSP datasets.

2013-12-02 - Created by Jonathan Sick
"""

import os
import glob


def _instr_name(band):
    """Map instrument names to bands."""
    if band in ["f475w", "f814w"]:
        instr = "acs-wfc"
    elif band in ["f110w", "f160w"]:
        instr = "wfc3-ir"
    elif band in ["f275w", "f336w"]:
        instr = "wf3-uvis"
    return instr


def _phat_basedir(brick):
    """Base directory for PHAT brick data"""
    return os.path.join(os.getenv('PHATDATA', None), "brick%02i" % brick)


def phat_phot_path(brick, field, filterset, kind='gst'):
    """Get path to a photometry product for a specific phat field.
    
    Parameters
    ----------

    brick : int
        Number of the brick (1-23).
    field : int
        Number of the field within the brick.
    filterset : str
        Name of the filter set: ``f275w-f336w``.
    """
    paths = glob.glob(os.path.join(_phat_basedir(brick),
        "*-b%02i-f%02i_%s_v1_%s.fits" % (brick, field, filterset, kind)))
    assert len(paths) == 1
    assert os.path.exists(paths[0])
    return paths[0]


def phat_brick_path(brick, band):
    """Get path to the drizzled FITS image for a PHAT brick.
    
    Parameters
    ----------

    brick : int
        Number of the brick (1-23).
    band : str
        Name of the filter: e.g. ``f275w``.
    """
    prefix = "hlsp_phat_hst"
    b = "*-m31-b%02i" % brick
    postfix = "v1_drz.fits"
    instr = _instr_name(band)
    filename = "_".join((prefix, instr, b, band, postfix))
    temp = os.path.join(_phat_basedir(brick), filename)
    paths = glob.glob(temp)
    assert len(paths) == 1
    assert os.path.exists(paths[0])
    return paths[0]


def phat_field_path(brick, field, band):
    """Get path to the drizzled FITS image for a specific PHAT field.
    
    Parameters
    ----------

    brick : int
        Number of the brick (1-23).
    field : int
        Number of the field within the brick.
    band : str
        Name of the filter: e.g. ``f275w``.
    """
    prefix = "hlsp_phat_hst"
    b = "*-m31-b%02i-f%02i" % (brick, field)
    postfix = "v1_drz.fits"
    instr = _instr_name(band)
    filename = "_".join((prefix, instr, b, band, postfix))
    paths = glob.glob(os.path.join(_phat_basedir(brick), filename))
    assert len(paths) == 1
    assert os.path.exists(paths[0])
    return paths[0]


def brown_phot_path(field, kind='cat'):
    """Get path for a Brown GO-10265 HLSP photometry product.
    
    Parameters
    ----------
    field : str
        Field name: halo11, stream, disk, halo21, halo35a, halo35b
    kind : str
        Data type. `cat` for photometry catalog, `art` for artificial stars
        and `msk` for a mask image.
    """
    if kind == 'cat':
        ext = '_v2_cat.txt'
    elif kind == 'art':
        ext = '_v2_art.fits'
    elif kind == 'msk':
        ext = '_v2_msk.fits'
    path = os.path.join(os.getenv('BROWNDATA', None),
            'hlsp_andromeda_hst_acs-wfc_%s_f606w-f814w%s' % (field, ext))
    assert os.path.exists(path)
    return path


def brown_image_path(field, band):
    """Get path for a Brown GO-10265 HLSP drizzled image product.
    
    Parameters
    ----------
    field : str
        Field name: halo11, stream, disk, halo21, halo35a, halo35b
    band : str
        Filter name. Either f814w or f606w.
    """
    path = os.path.join(os.getenv('BROWNDATA', None),
            'hlsp_andromeda_hst_acs-wfc_%s_%s_v2_img.fits' % (field, band))
    assert os.path.exists(path)
    return path


def main():
    pass


if __name__ == '__main__':
    main()
