#!/usr/bin/env python
# encoding: utf-8
"""
PHAT v2 artificial star tests.

2015-03-31 - Created by Jonathan Sick
"""

from astropy.table import Table

from m31hst.paths import phat_v2_ast_path


def load_phat_ast_table():
    """Read the PHAT v2 AST catalog.

    From http://cdsarc.u-strasbg.fr/vizier/ftp/cats/J/ApJS/215/9/ReadMe

    1- 11 F11.8   deg   RAdeg      Right Ascension in decimal degrees (J2000)
    13- 23 F11.8  deg   DEdeg      Declination in decimal degrees (J2000)
    25- 30 F6.3   mag   F275W-in   [14.1/36.9] Input HST/WFC3 F275W band mag
    32- 37 F6.3   mag   F275W-out  [14.1/25.4]?=99.999 Output HST/WFC3 F275W
    39- 44 F6.3   mag   F336W-in   [14.4/34.8] Input HST/WFC3 F336W band mag
    46- 51 F6.3   mag   F336W-out  ?=99.999 Output HST/WFC3 F336W band mag
    53- 58 F6.3   mag   F475W-in   Input HST/ACS F475W band magnitude
    60- 65 F6.3   mag   F475W-out  ?=99.999 Output HST/ACS F475W band mag
    67- 72 F6.3   mag   F814W-in   Input HST/ACS F814W band magnitude
    74- 79 F6.3   mag   F814W-out  ?=99.999 Output HST/ACS F814W band mag
    81- 86 F6.3   mag   F110W-in   ?=99.999 Input HST/WFC3 F110W band mag
    88- 93 F6.3   mag   F110W-out  ?=99.999 Output HST/WFC3 F110W band mag
    95-100 F6.3   mag   F160W-in   [13.5/27.3]?=99.999 Input HST/WFC3 F160W
    102-107 F6.3  mag   F160W-out [13.5/25.7]?=99.999 Output HST/WFC3 F160W
    """
    colnames = ['ra',
                'dec',
                'f275w_in',
                'f275w_out',
                'f336w_in',
                'f336w_out',
                'f475w_in',
                'f475w_out',
                'f814w_in',
                'f814w_out',
                'f110w_in',
                'f110w_out',
                'f160w_in',
                'f160w_out']
    t = Table.read(phat_v2_ast_path(),
                   format='ascii.no_header',
                   names=colnames,
                   guess=False,
                   delimiter=' ')
    return t
