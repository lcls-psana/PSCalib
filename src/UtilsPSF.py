#!/usr/bin/env python

import sys
import logging
logger = logging.getLogger(__name__)
from PSCalib.GeometryAccess import GeometryAccess

import numpy as np
from PSCalib.SegGeometryStore import sgs
#from Detector.GlobalUtils import print_ndarr, info_ndarr
#from PSCalib.GlobalUtils import CFRAME_LAB, CFRAME_PSANA


def get_psf(geo):
    """Returns array of vectors in CrystFEL format (psf stands for position-slow-fast vectors).
    """
    if not geo.valid: return None
    X, Y, Z = geo.get_pixel_coords() # pixel positions for top level object
    if X.size != 32*185*388: return None
    # For now it works for CSPAD only
    shape_cspad = (32,185,388)
    X.shape, Y.shape, Z.shape,  = shape_cspad, shape_cspad, shape_cspad

    psf = []

    for s in range(32):
        vp = (X[s,0,0], Y[s,0,0], Z[s,0,0])

        vs = (X[s,1,0]-X[s,0,0], \
              Y[s,1,0]-Y[s,0,0], \
              Z[s,1,0]-Z[s,0,0])

        vf = (X[s,0,1]-X[s,0,0], \
              Y[s,0,1]-Y[s,0,0], \
              Z[s,0,1]-Z[s,0,0])

        psf.append((vp,vs,vf))

    return psf


def print_psf(geo):
    """ Gets and prints psf array for test purpose.
    """
    if not geo.valid: return None
    psf = np.array(geo.get_psf(geo))
    s = 'print_psf(): psf.shape: %s \npsf vectors:' % (str(psf.shape))
    for (px,py,pz), (sx,xy,xz), (fx,fy,fz) in psf:
        s += '\n    p=(%12.2f, %12.2f, %12.2f),    s=(%8.2f, %8.2f, %8.2f)   f=(%8.2f, %8.2f, %8.2f)' \
              % (px,py,pz,  sx,xy,xz,  fx,fy,fz)
    logger.info(s)

