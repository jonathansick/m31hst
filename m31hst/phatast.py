#!/usr/bin/env python
# encoding: utf-8
"""
PHAT v2 artificial star tests.

2015-03-31 - Created by Jonathan Sick
"""

import numpy as np
from sklearn.cluster import KMeans
from astropy.table import Table
from astroML.stats import binned_statistic_2d
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


class PhatAstTable(object):
    """Data structure for the PHAT AST results."""
    def __init__(self):
        super(PhatAstTable, self).__init__()
        self.t = load_phat_ast_table()
        cluster_centers, self.labels = self._label_stars()
        self._define_fields(cluster_centers, self.labels)

    def _label_stars(self):
        km = KMeans(n_clusters=6)
        xy = np.vstack((self.t['ra'], self.t['dec'])).T
        km.fit(xy)
        return km.cluster_centers_, km.labels_

    def _define_fields(self, cluster_centers, labels):
        # Pre-baked list of centers, ordered sanely
        known_centers = [[11.55581084, 42.14674574],
                         [11.15978774, 41.63931688],
                         [10.87125638, 41.45011536],
                         [10.80073952, 41.31165493],
                         [10.70681719, 41.26110849],
                         [10.68679924, 41.30852815]]
        self.fields = []
        for c in known_centers:
            dists = np.hypot(c[0] - cluster_centers[:, 0],
                             c[1] - cluster_centers[:, 1])
            i = np.argmin(dists)
            d = {'center': c,
                 'label': i}
            self.fields.append(d)

    def write_crowdfile_for_field(self, path, fieldnum,
                                  bands=('f275w', 'f336w', 'f475w',
                                         'f814w', 'f110w', 'f160w')):
        """Write a StarFISH-compatible crowding file.

        Parameters
        ----------
        path : str
            Filepath where the crowdfile will be written.
        fieldnum : int
            Index of the PHAT AST fields to use (0-5).
        bands : list
            List of bands (in order) to include in the crowdfile.
        """
        label = self.fields[fieldnum]['label']
        sel = np.where(self.labels == label)[0]
        cols = [self.t['ra'][sel], self.t['dec'][sel]]
        fmt = ['%.8f', '%.8f']
        for band in bands:
            inkey = "{0}_in".format(band.lower())
            outkey = "{0}_out".format(band.lower())
            diffs = self.t[inkey][sel] - self.t[outkey][sel]
            dropped = np.where(np.abs(diffs) > 9.)[0]
            indata = np.array(self.t[inkey][sel])
            diffdata = np.array(diffs)
            diffdata[dropped] = 9.99
            cols.append(indata)
            cols.append(diffdata)
            fmt.append('%2.2f')
            fmt.append('%+1.2f')
        crowddata = np.vstack(cols).T
        np.savetxt(path, crowddata,
                   delimiter=' ',
                   fmt=fmt)

    def band_key_in(self, band):
        return "{0}_in".format(band.lower())

    def band_key_out(self, band):
        return "{0}_out".format(band.lower())

    def completeness_hess(self, fieldnum, band,
                          x_mag, y_mag, xlim, ylim, dmag):
        """Make a Hess diagram of completeness acros the plane."""
        label = self.fields[fieldnum]['label']
        s = np.where(self.labels == label)[0]
        tt = self.t[s]

        if isinstance(y_mag, basestring):
            # a single mag
            y = tt[self.band_key_in(y_mag)]
        else:
            b1, b2 = y_mag
            y = tt[self.band_key_in(b1)] - tt[self.band_key_in(b2)]

        if isinstance(x_mag, basestring):
            # a single mag
            x = tt[self.band_key_in(x_mag)]
        else:
            b1, b2 = x_mag
            x = tt[self.band_key_in(b1)] - tt[self.band_key_in(b2)]

        # bin the number of stars into the hess plane and the number of
        # recovered stars to get the completeness fraction
        def _completeness(values):
            v = np.array(values)
            if len(v) == 0:
                return np.nan
            else:
                return float(np.where(v < 90.)[0].shape[0]) / v.shape[0]

        # extend stop so it is included; len(edges) is nx+1
        x_grid = np.arange(min(xlim), max(xlim) + dmag / 2., dmag)
        y_grid = np.arange(min(ylim), max(ylim) + dmag / 2., dmag)
        H, x_edges, y_edges = binned_statistic_2d(x, y,
                                                  tt[self.band_key_out(band)],
                                                  statistic=_completeness,
                                                  bins=[x_grid, y_grid])
        return H.T, x_edges, y_edges

    def error_hess(self, fieldnum, band,
                   x_mag, y_mag, xlim, ylim, dmag):
        """Make a Hess diagram of the mean error across the Hess plane."""
        label = self.fields[fieldnum]['label']
        s = np.where(self.labels == label)[0]
        tt = self.t[s]

        if isinstance(y_mag, basestring):
            # a single mag
            y = tt[self.band_key_in(y_mag)]
        else:
            b1, b2 = y_mag
            y = tt[self.band_key_in(b1)] - tt[self.band_key_in(b2)]

        if isinstance(x_mag, basestring):
            # a single mag
            x = tt[self.band_key_in(x_mag)]
        else:
            b1, b2 = x_mag
            x = tt[self.band_key_in(b1)] - tt[self.band_key_in(b2)]

        # extend stop so it is included; len(edges) is nx+1
        x_grid = np.arange(min(xlim), max(xlim) + dmag / 2., dmag)
        y_grid = np.arange(min(ylim), max(ylim) + dmag / 2., dmag)
        diff = tt[self.band_key_in(band)] - tt[self.band_key_out(band)]

        def filtered_sigma(vals):
            """Filter out the dropped stars from sigma computation."""
            s = np.where(np.abs(vals) < 20.)[0]
            return np.std(vals[s])

        H, x_edges, y_edges = binned_statistic_2d(x, y,
                                                  diff,
                                                  statistic=filtered_sigma,
                                                  bins=[x_grid, y_grid])
        return H.T, x_edges, y_edges
