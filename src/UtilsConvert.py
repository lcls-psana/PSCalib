#!/usr/bin/env python

import sys
import logging
logger = logging.getLogger(__name__)
from PSCalib.GeometryAccess import GeometryAccess

import numpy as np
from PSCalib.SegGeometryStore import sgs
from Detector.GlobalUtils import print_ndarr, info_ndarr

#----------

def header_crystfel():
    return\
    '\n; Geometry constants generated by genuine psana'\
    '\n'\
    '\n; --- VALUES YOU MAY WANT TO FILL IN MANUALLY ---'\
    '\n'\
    '\nclen =  /LCLS/detector_1/EncoderValue'\
    '\nphoton_energy = /LCLS/photon_energy_eV'\
    '\nadu_per_eV = 0.1'\
    '\n'\
    '\ndata = /entry_1/data_1/data'\
    '\n'\
    '\ndim0 = %'\
    '\ndim1 = ss'\
    '\ndim2 = fs'\
    '\n'\
    '\n; mask = /entry_1/data_1/mask'\
    '\n; mask_good = 0x0000'\
    '\n; mask_bad = 0xffff'

#----------

"""
# per asic info:

p15a1/fs = -0.000000x +1.000000y
p15a1/ss = -1.000000x +0.000000y
p15a1/res = 10000.000             # resolution 1m / <pixel-size>
p15a1/corner_x = 2.500000
p15a1/corner_y = -628.500000
p15a1/coffset = 1.000000          # z-offset correction
p15a1/min_fs = 192
p15a1/max_fs = 383
p15a1/min_ss = 5280
p15a1/max_ss = 5455
p15a1/no_index = 0                # exclude panels from indexing
"""

def panel_constants_to_crystfel(seg, n, x, y, z):
    """Formats psana constants to CrystFEL format
       Parameters:
       - seg [SegGeometry] - segment eometry object
       - n [int] - segment number in daq array for detector
       - x, y, z [float] - pixel coordimane arrays (in the detector geometry) for single panel
    """

    arows, acols = seg.asic_rows_cols()
    ssize = seg.size()
    srows, scols = seg.shape()
    pix_size = seg.pixel_scale_size()
    nasics_in_rows, nasics_in_cols = seg.number_of_asics_in_rows_cols()
    nasicsf = nasics_in_cols

    logger.debug(info_ndarr(x, name='  panel %02d x'%n, first=0, last=3))
    logger.debug(info_ndarr(y, name='  panel %02d y'%n, first=0, last=3))

    txt = '\n'
    for a,(r0,c0) in enumerate(seg.asic0indices()):

        vfs = np.array((\
               x[r0,c0+acols-1] - x[r0,c0],\
               y[r0,c0+acols-1] - y[r0,c0],\
               z[r0,c0+acols-1] - z[r0,c0]))
        vss = np.array((\
               x[r0+arows-1,c0] - x[r0,c0],\
               y[r0+arows-1,c0] - y[r0,c0],\
               z[r0+arows-1,c0] - z[r0,c0]))
        nfs = vfs/np.linalg.norm(vfs)
        nss = vss/np.linalg.norm(vss)

        pref = '\np%da%d'%(n,a)

        txt +='%s/fs = %+.6fx %+.6fy %+.6fz' % (pref, nfs[0], nfs[1], nfs[2])\
            + '%s/ss = %+.6fx %+.6fy %+.6fz' % (pref, nfs[0], nfs[1], nfs[2])\
            + '%s/res = %.3f' % (pref, 1e6/pix_size)\
            + '%s/corner_x = %.6f' % (pref, x[r0,c0]/pix_size)\
            + '%s/corner_y = %.6f' % (pref, y[r0,c0]/pix_size)\
            + '%s/coffset = 0' % (pref)\
            + '%s/min_fs = %d' % (pref, (a%nasicsf)*acols)\
            + '%s/max_fs = %d' % (pref, (a%nasicsf+1)*acols-1)\
            + '%s/min_ss = %d' % (pref, n*srows + (a//nasicsf)*arows)\
            + '%s/max_ss = %d' % (pref, n*srows + (a//nasicsf+1)*arows - 1)\
            + '%s/no_index = 0' % (pref)\
            + '\n'

    return txt

#----------

def geometry_to_crystfel(seg, valid_nsegs, fname, ofname=None):

    asic0inds = seg.asic0indices()
    arows, acols = seg.asic_rows_cols()
    ssize = seg.size()
    srows, scols = seg.shape()
    pix_size = seg.pixel_scale_size()
    nasics_in_rows, nasics_in_cols = seg.number_of_asics_in_rows_cols()

    print('name', seg.name())
    print('asic0ind', asic0inds)
    print('arows, acols', arows, acols)
    print('ssize', ssize)
    print('seg.shape()', seg.shape())
    print('pix_size', pix_size)
    print('nasics_in_rows, nasics_in_cols', nasics_in_rows, nasics_in_cols)

    geo = GeometryAccess(fname, 0, use_wide_pix_center=False)
    x, y, z = geo.get_pixel_coords(oname=None, oindex=0, do_tilt=True)
    print_ndarr(x, name='x', first=0, last=10)
    print_ndarr(y, name='y', first=0, last=10)

    nsegs = x.size/seg.size()
    print('nsegs in geometry', nsegs)
    assert nsegs in valid_nsegs, 'number of %s segments %d should be in %s' % (seg.name(), nsegs, str(valid_nsegs))

    shape = (nsegs, srows, scols)
    print('geo shape', shape)

    x.shape = shape
    y.shape = shape
    z.shape = shape

    txt = header_crystfel()
    for n in range(nsegs):
        txt += panel_constants_to_crystfel(seg, n, x[n,:], y[n,:], z[n,:])

    logger.info(txt)

    if ofname is not None:
        f = open(ofname,'w')
        f.write(txt)
        f.close()
        logger.info('geometry constants in CrystFEL format saved in: %s' % ofname)

#----------

def convert_detector_any(dettype, fname, ofname):
    if   'epix10ka' in dettype.lower(): geometry_to_crystfel(sgs.Create(segname='EPIX10KA:V1',pbits=0), (1,4,16), fname, ofname)
    elif 'jungfrau' in dettype.lower(): geometry_to_crystfel(sgs.Create(segname='JUNGFRAU:V1',pbits=0), (1,2,8),  fname, ofname)
    elif 'cspad'    in dettype.lower(): geometry_to_crystfel(sgs.Create(segname='SENS2X1:V1', pbits=0), (1,8,32), fname, ofname)
    else: logger.warning('NON_IMPLEMENTED DETECTOR TYPE: %s' % dettype)

#----------

if __name__ == "__main__":

    def test_epix10ka_any(fname, ofname='geo_epix10ka_crystfel.txt'):
        geometry_to_crystfel(sgs.Create(segname='EPIX10KA:V1',pbits=0), (1,4,16), fname, ofname)

    def test_jungfrau_any(fname, ofname='geo_jungfrau_crystfel.txt'):
        geometry_to_crystfel(sgs.Create(segname='JUNGFRAU:V1',pbits=0), (1,2,8), fname, ofname)

    def test_cspad_any(fname, ofname='geo_cspad_crystfel.txt'):
        geometry_to_crystfel(sgs.Create(segname='SENS2X1:V1',pbits=0), (1,8,32), fname, ofname)

#----------

if __name__ == "__main__":

    #import pyimgalgos.GlobalGraphics as gg

    #print dir(logging)
    #print logging._levelNames
    DICT_NAME_TO_LEVEL = logging._levelNames # logging._nameToLevel # {'INFO': 20, 'WARNING': 30, 'WARN': 30,...
    LEVEL_NAMES = [v for v in logging._levelNames.values() if isinstance(v,str)] #_levelToName
    STR_LEVEL_NAMES = ', '.join(LEVEL_NAMES)

    scrname = sys.argv[0].rsplit('/')[-1]

    fname_jungfrau_8     = '/reg/g/psdm/detector/data2_test/geometry/geo-jungfrau-8-segment.data'
    fname_epix10ka2m_16  = '/reg/g/psdm/detector/data2_test/geometry/geo-epix10ka2m-16-segment.data'
    fname_epix10ka2m_def = '/reg/g/psdm/detector/data2_test/geometry/geo-epix10ka2m-default.data'
    fname_cspad_cxi      = '/reg/g/psdm/detector/data2_test/geometry/geo-cspad-cxi.data'

    d_dettype = 'epix10ka'
    d_fname   = fname_epix10ka2m_16
    d_ofname  = 'geo-crystfel.txt'
    d_loglev  ='INFO'
    usage = '\nE.g.: %s' % scrname\
      + '\n  or: %s -t <test-number: 1,2,3,4,...>' % (scrname)\
      + '\n  or: %s -d epix10ka -f %s -o geo_crystfel.txt -l DEBUG' % (scrname, d_fname)

    import argparse

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-t', '--tname',   default='0',       type=str, help='test number: 1/2/3/4 = epix10ka/jungfrau/cspad/epix10ka-default')
    parser.add_argument('-d', '--dettype', default=d_dettype, type=str, help='detector type, i.e. epix10ka, jungfrau, cspad, def=%s' % d_dettype)
    parser.add_argument('-f', '--fname',   default=d_fname,   type=str, help='input geometry file name, def=%s' % d_fname)
    parser.add_argument('-o', '--ofname',  default=d_ofname,  type=str, help='output file name, def=%s' % d_ofname)
    parser.add_argument('-l', '--loglev',  default=d_loglev,  type=str, help='logging level name, one of %s, def=%s' % (STR_LEVEL_NAMES, d_loglev))
    #parser.add_argument('exp', type=str, help='experiment name (e.g. amox23616)')
    #parser.add_argument('run', type=int, help='run number') # 104

    args = parser.parse_args()
    print('Arguments:') #%s\n' % str(args))
    for k,v in vars(args).items(): print('  %12s : %s' % (k, str(v)))

    logging.basicConfig(format='[%(levelname).1s] L%(lineno)04d : %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=DICT_NAME_TO_LEVEL[args.loglev])
    logging.debug('Logger is initialized for level %s' % args.loglev)

    tname = args.tname

    if   tname=='0': convert_detector_any(args.dettype, args.fname, args.ofname)
    elif tname=='1': test_epix10ka_any(fname_epix10ka2m_16)
    elif tname=='2': test_jungfrau_any(fname_jungfrau_8)
    elif tname=='3': test_cspad_any(fname_cspad_cxi)
    elif tname=='4': test_epix10ka_any(fname_epix10ka2m_def)
    else: logger.warning('NON-IMPLEMENTED TEST: %s' % tname)

    sys.exit('END OF %s' % scrname)

#----------
